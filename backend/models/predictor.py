"""Model prediction logic for the Fake News Detector."""

import os
import joblib
import logging
import numpy as np
from data.preprocessor import TextPreprocessor

logger = logging.getLogger(__name__)


class FakeNewsPredictor:
    """Handles prediction of fake news using trained models."""
    
    def __init__(self, model_path=None, vectorizer_path=None):
        """Initialize the predictor.
        
        Args:
            model_path (str): Path to the trained model
            vectorizer_path (str): Path to the trained vectorizer
        """
        self.model = None
        self.vectorizer = None
        self.preprocessor = TextPreprocessor()
        self.model_info = {}
        
        if model_path and vectorizer_path:
            self.load_model(model_path, vectorizer_path)
    
    def load_model(self, model_path, vectorizer_path):
        """Load the trained model and vectorizer.
        
        Args:
            model_path (str): Path to the trained model
            vectorizer_path (str): Path to the trained vectorizer
        """
        try:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            if not os.path.exists(vectorizer_path):
                raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
            
            # Load model and vectorizer
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            
            # Store model information
            self.model_info = {
                'model_type': type(self.model).__name__,
                'model_path': model_path,
                'vectorizer_path': vectorizer_path,
                'feature_count': self.vectorizer.vocabulary_.__len__() if hasattr(self.vectorizer, 'vocabulary_') else 'Unknown',
                'model_loaded': True
            }
            
            logger.info(f"Model loaded successfully from {model_path}")
            logger.info(f"Vectorizer loaded successfully from {vectorizer_path}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None
            self.vectorizer = None
            raise
    
    def predict(self, text):
        """Predict if a news article is fake or real.
        
        Args:
            text (str): News article text to analyze
            
        Returns:
            tuple: (prediction, confidence) where prediction is 'real' or 'fake'
                  and confidence is a float between 0 and 1
        """
        if self.model is None or self.vectorizer is None:
            raise ValueError("Model and vectorizer must be loaded before making predictions")
        
        try:
            # Preprocess the text
            processed_text = self.preprocessor.preprocess_text(text)
            
            # Vectorize the text
            text_vector = self.vectorizer.transform([processed_text])
            
            # Make prediction
            prediction_proba = self.model.predict_proba(text_vector)[0]
            prediction_binary = self.model.predict(text_vector)[0]
            
            # Convert binary prediction to label
            prediction_label = 'fake' if prediction_binary == 1 else 'real'
            
            # Get confidence (probability of the predicted class)
            confidence = prediction_proba[prediction_binary]
            
            logger.debug(f"Prediction: {prediction_label}, Confidence: {confidence:.4f}")
            
            return prediction_label, float(confidence)
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise
    
    def predict_batch(self, texts):
        """Predict for multiple texts at once.
        
        Args:
            texts (list): List of news article texts to analyze
            
        Returns:
            list: List of tuples (prediction, confidence) for each text
        """
        if self.model is None or self.vectorizer is None:
            raise ValueError("Model and vectorizer must be loaded before making predictions")
        
        try:
            # Preprocess all texts
            processed_texts = [self.preprocessor.preprocess_text(text) for text in texts]
            
            # Vectorize all texts
            text_vectors = self.vectorizer.transform(processed_texts)
            
            # Make predictions
            predictions_proba = self.model.predict_proba(text_vectors)
            predictions_binary = self.model.predict(text_vectors)
            
            results = []
            for i, pred_binary in enumerate(predictions_binary):
                pred_label = 'fake' if pred_binary == 1 else 'real'
                confidence = float(predictions_proba[i][pred_binary])
                results.append((pred_label, confidence))
            
            logger.info(f"Batch prediction completed for {len(texts)} texts")
            return results
            
        except Exception as e:
            logger.error(f"Error during batch prediction: {e}")
            raise
    
    def get_feature_importance(self, top_n=20):
        """Get top features that influence predictions.
        
        Args:
            top_n (int): Number of top features to return
            
        Returns:
            dict: Dictionary with 'fake' and 'real' features
        """
        if self.model is None or self.vectorizer is None:
            raise ValueError("Model and vectorizer must be loaded")
        
        try:
            # Get feature names and coefficients
            feature_names = self.vectorizer.get_feature_names_out()
            coefficients = self.model.coef_[0]
            
            # Get top features for fake news (positive coefficients)
            fake_indices = np.argsort(coefficients)[-top_n:][::-1]
            fake_features = [(feature_names[i], coefficients[i]) for i in fake_indices]
            
            # Get top features for real news (negative coefficients)
            real_indices = np.argsort(coefficients)[:top_n]
            real_features = [(feature_names[i], abs(coefficients[i])) for i in real_indices]
            
            return {
                'fake_indicators': fake_features,
                'real_indicators': real_features
            }
            
        except Exception as e:
            logger.error(f"Error getting feature importance: {e}")
            raise
    
    def get_model_info(self):
        """Get information about the loaded model.
        
        Returns:
            dict: Model information
        """
        return self.model_info
    
    def is_loaded(self):
        """Check if model and vectorizer are loaded.
        
        Returns:
            bool: True if both model and vectorizer are loaded
        """
        return self.model is not None and self.vectorizer is not None