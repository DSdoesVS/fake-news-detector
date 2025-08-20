"""
Prediction module for the Fake News Detector
"""

import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from utils.helpers import clean_text, validate_text_input, format_prediction_response
from data.preprocessor import TextPreprocessor

class FakeNewsPredictor:
    """
    Fake News Prediction class
    """
    
    def __init__(self, model_path=None, vectorizer_path=None):
        self.model = None
        self.vectorizer = None
        self.preprocessor = TextPreprocessor()
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.is_loaded = False
    
    def load_model(self, model_path=None, vectorizer_path=None):
        """
        Load the trained model and vectorizer
        """
        if model_path:
            self.model_path = model_path
        if vectorizer_path:
            self.vectorizer_path = vectorizer_path
        
        if not self.model_path or not self.vectorizer_path:
            # Use default paths
            base_dir = os.path.dirname(os.path.dirname(__file__))
            self.model_path = os.path.join(base_dir, 'models', 'fake_news_model.pkl')
            self.vectorizer_path = os.path.join(base_dir, 'models', 'tfidf_vectorizer.pkl')
        
        try:
            # Load model
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
            else:
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            # Load vectorizer
            if os.path.exists(self.vectorizer_path):
                with open(self.vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
            else:
                raise FileNotFoundError(f"Vectorizer file not found: {self.vectorizer_path}")
            
            self.is_loaded = True
            print("Model and vectorizer loaded successfully!")
            return True
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.is_loaded = False
            return False
    
    def predict(self, text, return_detailed=False):
        """
        Predict if the given text is fake or real news
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Validate input
        is_valid, errors = validate_text_input(text)
        if not is_valid:
            raise ValueError(f"Invalid input: {', '.join(errors)}")
        
        try:
            # Preprocess text
            processed_text = self.preprocessor.preprocess(text)
            
            # Vectorize text
            text_vector = self.vectorizer.transform([processed_text])
            
            # Make prediction
            prediction = self.model.predict(text_vector)[0]
            prediction_proba = self.model.predict_proba(text_vector)[0]
            
            # Get confidence score
            confidence = max(prediction_proba)
            
            if return_detailed:
                return format_prediction_response(
                    prediction, 
                    confidence, 
                    text,
                    {
                        'processed_text': processed_text,
                        'processed_length': len(processed_text),
                        'original_length': len(text),
                        'fake_probability': float(prediction_proba[0]),
                        'real_probability': float(prediction_proba[1])
                    }
                )
            else:
                return {
                    'prediction': 'REAL' if prediction == 1 else 'FAKE',
                    'confidence': float(confidence),
                    'prediction_label': int(prediction)
                }
                
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {str(e)}")
    
    def predict_batch(self, texts, return_detailed=False):
        """
        Predict multiple texts at once
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        results = []
        
        for i, text in enumerate(texts):
            try:
                result = self.predict(text, return_detailed)
                result['index'] = i
                results.append(result)
            except Exception as e:
                results.append({
                    'index': i,
                    'error': str(e),
                    'prediction': None,
                    'confidence': None
                })
        
        return results
    
    def get_feature_importance(self, text, top_n=10):
        """
        Get the most important features for prediction
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            # Preprocess text
            processed_text = self.preprocessor.preprocess(text)
            
            # Vectorize text
            text_vector = self.vectorizer.transform([processed_text])
            
            # Get feature names
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get coefficients
            coefficients = self.model.coef_[0]
            
            # Get non-zero features in the text
            non_zero_indices = text_vector.nonzero()[1]
            
            # Get feature importance for this text
            feature_importance = []
            for idx in non_zero_indices:
                feature_importance.append({
                    'feature': feature_names[idx],
                    'coefficient': float(coefficients[idx]),
                    'value': float(text_vector[0, idx])
                })
            
            # Sort by absolute coefficient value
            feature_importance.sort(key=lambda x: abs(x['coefficient']), reverse=True)
            
            return feature_importance[:top_n]
            
        except Exception as e:
            raise RuntimeError(f"Feature importance calculation failed: {str(e)}")
    
    def get_model_info(self):
        """
        Get information about the loaded model
        """
        if not self.is_loaded:
            return {"error": "Model not loaded"}
        
        try:
            info = {
                "model_type": type(self.model).__name__,
                "vectorizer_type": type(self.vectorizer).__name__,
                "model_path": self.model_path,
                "vectorizer_path": self.vectorizer_path,
                "is_loaded": self.is_loaded
            }
            
            # Add model-specific info
            if hasattr(self.model, 'classes_'):
                info["classes"] = self.model.classes_.tolist()
            
            if hasattr(self.model, 'coef_'):
                info["num_features"] = len(self.model.coef_[0])
            
            if hasattr(self.vectorizer, 'vocabulary_'):
                info["vocabulary_size"] = len(self.vectorizer.vocabulary_)
            
            return info
            
        except Exception as e:
            return {"error": str(e)}

# Global predictor instance
predictor = FakeNewsPredictor()
