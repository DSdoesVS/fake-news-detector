"""
Main Flask application for the Fake News Detector API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import pickle
import nltk
from textblob import TextBlob
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables for model and vectorizer
model = None
vectorizer = None
model_loaded = False

def ensure_model_loaded():
    """Ensure model is loaded before processing requests"""
    global model, vectorizer, model_loaded
    if not model_loaded:
        load_model()

# Global variables for model and vectorizer
model = None
vectorizer = None
model_loaded = False

def preprocess_text(text):
    """
    Preprocess text for machine learning model
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove punctuation and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def load_model():
    """
    Load the trained model and vectorizer
    """
    global model, vectorizer, model_loaded
    
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'fake_news_model.pkl')
    vectorizer_path = os.path.join(os.path.dirname(__file__), 'models', 'tfidf_vectorizer.pkl')
    
    print(f"Looking for model at: {model_path}")
    print(f"Looking for vectorizer at: {vectorizer_path}")
    print(f"Model file exists: {os.path.exists(model_path)}")
    print(f"Vectorizer file exists: {os.path.exists(vectorizer_path)}")
    
    try:
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            with open(vectorizer_path, 'rb') as f:
                vectorizer = pickle.load(f)
            model_loaded = True
            print("Model and vectorizer loaded successfully!")
            print(f"Model type: {type(model)}")
            print(f"Vectorizer type: {type(vectorizer)}")
            return True
        else:
            print("Model files not found. Please train the model first.")
            print(f"Model path: {model_path}")
            print(f"Vectorizer path: {vectorizer_path}")
            model_loaded = False
            return False
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        import traceback
        traceback.print_exc()
        model_loaded = False
        return False

@app.route('/')
def home():
    """
    Home endpoint
    """
    return jsonify({
        "message": "Fake News Detector API",
        "version": "1.0",
        "endpoints": {
            "/predict": "POST - Predict if news is fake or real",
            "/health": "GET - Health check"
        }
    })

@app.route('/health')
def health():
    """
    Health check endpoint
    """
    ensure_model_loaded()
    return jsonify({
        "status": "healthy",
        "model_loaded": model_loaded and model is not None and vectorizer is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict if news article is fake or real
    """
    try:
        # Ensure model is loaded
        ensure_model_loaded()
        
        # Get data from request
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "error": "No text provided. Please send a JSON object with 'text' field."
            }), 400
        
        text = data['text']
        
        if not text or len(text.strip()) == 0:
            return jsonify({
                "error": "Empty text provided."
            }), 400
        
        # Check if model is loaded
        if not model_loaded or model is None or vectorizer is None:
            return jsonify({
                "error": "Model not loaded. Please train the model first."
            }), 503
        
        # Preprocess text
        processed_text = preprocess_text(text)
        
        # Vectorize text
        text_vector = vectorizer.transform([processed_text])
        
        # Make prediction
        prediction = model.predict(text_vector)[0]
        prediction_proba = model.predict_proba(text_vector)[0]
        
        # Get confidence score
        confidence = max(prediction_proba)
        
        # Prepare result
        result = {
            "prediction": "REAL" if prediction == 1 else "FAKE",
            "confidence": float(confidence),
            "confidence_percentage": f"{confidence * 100:.2f}%",
            "processed_text_length": len(processed_text),
            "original_text_length": len(text)
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "error": f"An error occurred during prediction: {str(e)}"
        }), 500

@app.route('/train', methods=['POST'])
def train_model_endpoint():
    """
    Trigger model training (for development purposes)
    """
    try:
        from models.train_model import train_and_save_model
        
        result = train_and_save_model()
        
        if result:
            # Reload the model
            load_model()
            return jsonify({
                "message": "Model trained and saved successfully!",
                "model_loaded": model is not None and vectorizer is not None
            })
        else:
            return jsonify({
                "error": "Failed to train model. Check logs for details."
            }), 500
            
    except ImportError:
        return jsonify({
            "error": "Training module not found. Please check if train_model.py exists."
        }), 500
    except Exception as e:
        return jsonify({
            "error": f"An error occurred during training: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Download required NLTK data
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
    except:
        pass
    
    # Load model on startup
    load_model()
    
    # Run the app
    app.run(debug=False, host='0.0.0.0', port=5000)
