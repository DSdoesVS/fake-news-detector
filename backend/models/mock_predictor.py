"""Mock model for testing when dependencies are not available."""

import os
import json
import random
import logging
from datetime import datetime
from data.simple_preprocessor import SimpleTextPreprocessor

logger = logging.getLogger(__name__)


class MockPredictor:
    """Mock predictor for testing without actual ML dependencies."""
    
    def __init__(self, model_path=None, vectorizer_path=None):
        """Initialize mock predictor."""
        self.preprocessor = SimpleTextPreprocessor()
        self.model_info = {
            'model_type': 'MockLogisticRegression',
            'model_path': model_path or 'mock_model.json',
            'vectorizer_path': vectorizer_path or 'mock_vectorizer.json',
            'feature_count': 10000,
            'model_loaded': True
        }
        logger.info("Mock predictor initialized for testing")
    
    def predict(self, text):
        """Mock prediction based on simple heuristics."""
        if not text or not isinstance(text, str):
            raise ValueError("Invalid text input")
        
        # Preprocess the text
        processed_text = self.preprocessor.preprocess_text(text)
        
        # Simple heuristics for fake news detection
        fake_keywords = [
            'breaking', 'urgent', 'shocking', 'exclusive', 'bombshell',
            'incredible', 'miraculous', 'secret', 'exposed', 'government',
            'pharma', 'aliens', 'time', 'traveler', 'weird', 'trick',
            'doctors', 'hate', 'scientists', 'baffled', 'want', 'know'
        ]
        
        text_lower = text.lower()
        processed_lower = processed_text.lower()
        fake_score = 0
        
        # Count fake indicators in original text
        for keyword in fake_keywords:
            if keyword in text_lower:
                fake_score += 1
        
        # Additional heuristics
        if text.count('!') > 3:  # Too many exclamation marks
            fake_score += 2
        
        # Count uppercase words
        uppercase_words = sum(1 for word in text.split() if word.isupper() and len(word) > 1)
        if uppercase_words > len(text.split()) * 0.2:  # Too many caps
            fake_score += 1
        
        if any(phrase in text_lower for phrase in ['click here', 'share this', 'you won\'t believe']):
            fake_score += 2
        
        # Check for sensational language
        sensational_phrases = ['amazing', 'incredible', 'unbelievable', 'shocking', 'stunning']
        sensational_count = sum(1 for phrase in sensational_phrases if phrase in text_lower)
        if sensational_count > 2:
            fake_score += 1
        
        # Calculate prediction
        total_words = len(text.split())
        fake_ratio = fake_score / max(total_words / 15, 1)  # Normalize by text length
        
        # Add some randomness for realism but keep it consistent for same text
        random.seed(hash(text) % 2147483647)  # Use text hash as seed for consistency
        random_factor = random.uniform(-0.05, 0.05)
        
        # Calculate confidence based on fake indicators
        base_confidence = 0.6 + fake_ratio * 0.25 + random_factor
        confidence = min(max(base_confidence, 0.15), 0.95)
        
        if fake_ratio > 0.4:
            prediction = 'fake'
        else:
            prediction = 'real'
            confidence = 1 - confidence  # Invert for real news
        
        logger.debug(f"Mock prediction: {prediction} (confidence: {confidence:.4f}, fake_score: {fake_score})")
        return prediction, float(confidence)
    
    def get_model_info(self):
        """Get mock model information."""
        return self.model_info
    
    def is_loaded(self):
        """Mock model is always loaded."""
        return True


def create_mock_model_files():
    """Create mock model files for testing."""
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    
    # Mock model file
    mock_model = {
        'type': 'MockLogisticRegression',
        'created': datetime.now().isoformat(),
        'features': 10000,
        'accuracy': 0.85
    }
    
    with open(os.path.join(model_dir, 'trained_model.json'), 'w') as f:
        json.dump(mock_model, f, indent=2)
    
    # Mock vectorizer file
    mock_vectorizer = {
        'type': 'MockTfidfVectorizer',
        'vocabulary_size': 10000,
        'created': datetime.now().isoformat()
    }
    
    with open(os.path.join(model_dir, 'vectorizer.json'), 'w') as f:
        json.dump(mock_vectorizer, f, indent=2)
    
    logger.info("Mock model files created for testing")


if __name__ == '__main__':
    # Create mock model files for testing
    create_mock_model_files()
    
    # Test the mock predictor
    predictor = MockPredictor()
    
    # Test with fake news example
    fake_text = "BREAKING: Government officials confirm alien contact established last week!"
    prediction, confidence = predictor.predict(fake_text)
    print(f"Fake text prediction: {prediction} ({confidence:.2f})")
    
    # Test with real news example
    real_text = "Scientists at MIT have developed a new battery technology for electric vehicles."
    prediction, confidence = predictor.predict(real_text)
    print(f"Real text prediction: {prediction} ({confidence:.2f})")