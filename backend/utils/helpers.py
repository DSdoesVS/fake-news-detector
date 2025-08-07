"""Utility functions for the Fake News Detector backend."""

import re
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_text_input(text, max_length=10000):
    """Validate text input for prediction.
    
    Args:
        text (str): Text to validate
        max_length (int): Maximum allowed text length
        
    Returns:
        str or None: Error message if validation fails, None if valid
    """
    if not text:
        return "Text cannot be empty"
    
    if not isinstance(text, str):
        return "Text must be a string"
    
    # Check length
    if len(text) > max_length:
        return f"Text too long. Maximum {max_length} characters allowed, got {len(text)}"
    
    # Check if text is too short to be meaningful
    if len(text.strip()) < 10:
        return "Text too short. Please provide at least 10 characters"
    
    # Check if text contains mostly non-alphabetic characters
    alpha_chars = sum(c.isalpha() for c in text)
    if alpha_chars / len(text) < 0.3:
        return "Text must contain at least 30% alphabetic characters"
    
    return None


def format_prediction_response(prediction, confidence, original_text=None):
    """Format prediction results into a standardized response.
    
    Args:
        prediction (str): Prediction result ('real' or 'fake')
        confidence (float): Confidence score (0-1)
        original_text (str, optional): Original input text
        
    Returns:
        dict: Formatted response
    """
    response = {
        'prediction': prediction,
        'confidence': round(confidence, 4),
        'confidence_percentage': round(confidence * 100, 2),
        'timestamp': datetime.utcnow().isoformat(),
        'is_fake': prediction == 'fake'
    }
    
    # Add confidence level interpretation
    if confidence >= 0.8:
        confidence_level = 'high'
    elif confidence >= 0.6:
        confidence_level = 'medium'
    else:
        confidence_level = 'low'
    
    response['confidence_level'] = confidence_level
    
    # Add text statistics if original text is provided
    if original_text:
        response['text_stats'] = {
            'character_count': len(original_text),
            'word_count': len(original_text.split()),
            'sentence_count': len(re.split(r'[.!?]+', original_text))
        }
    
    return response


def sanitize_text(text):
    """Sanitize text for safe processing and display.
    
    Args:
        text (str): Text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not isinstance(text, str):
        return ""
    
    # Remove potential HTML/script tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove potential SQL injection patterns
    text = re.sub(r'(\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b)', '', text, flags=re.IGNORECASE)
    
    # Limit consecutive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def calculate_text_complexity(text):
    """Calculate various complexity metrics for text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Complexity metrics
    """
    if not isinstance(text, str) or not text:
        return {'error': 'Invalid text input'}
    
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Basic metrics
    word_count = len(words)
    sentence_count = len(sentences)
    char_count = len(text)
    
    # Average metrics
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    # Vocabulary diversity (unique words / total words)
    unique_words = set(word.lower() for word in words)
    vocabulary_diversity = len(unique_words) / word_count if word_count > 0 else 0
    
    return {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'character_count': char_count,
        'avg_word_length': round(avg_word_length, 2),
        'avg_sentence_length': round(avg_sentence_length, 2),
        'vocabulary_diversity': round(vocabulary_diversity, 3),
        'unique_words': len(unique_words)
    }


def log_prediction_request(text, prediction, confidence, user_id=None):
    """Log prediction requests for monitoring and analysis.
    
    Args:
        text (str): Input text
        prediction (str): Prediction result
        confidence (float): Confidence score
        user_id (str, optional): User identifier
    """
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'prediction': prediction,
        'confidence': confidence,
        'text_length': len(text),
        'user_id': user_id or 'anonymous'
    }
    
    logger.info(f"Prediction logged: {log_data}")


def create_error_response(message, error_code=None):
    """Create standardized error response.
    
    Args:
        message (str): Error message
        error_code (str, optional): Error code for categorization
        
    Returns:
        dict: Error response
    """
    response = {
        'error': message,
        'timestamp': datetime.utcnow().isoformat(),
        'success': False
    }
    
    if error_code:
        response['error_code'] = error_code
    
    return response


def benchmark_prediction_time(func):
    """Decorator to benchmark prediction execution time.
    
    Args:
        func: Function to benchmark
        
    Returns:
        function: Decorated function
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        logger.info(f"Prediction executed in {execution_time:.4f} seconds")
        
        return result
    
    return wrapper


def extract_key_phrases(text, max_phrases=10):
    """Extract potential key phrases from text.
    
    Args:
        text (str): Text to analyze
        max_phrases (int): Maximum number of phrases to return
        
    Returns:
        list: List of potential key phrases
    """
    if not isinstance(text, str) or not text:
        return []
    
    # Simple approach: find common patterns that might indicate fake news
    fake_indicators = [
        r'\bBREAKING\b',
        r'\bURGENT\b',
        r'\bSHOCKING\b',
        r'\bEXCLUSIVE\b',
        r'\bBOMBSHELL\b',
        r'\bINCREDIBLE\b',
        r'\bMIRACULOUS\b',
        r'\bALERT\b',
        r'\bEXPOSED\b',
        r'\bsecret\b.*\bthat\b.*\bdoesn\'t want you to know\b',
        r'\bgovernment\b.*\bcover.*up\b',
        r'\bbig pharma\b',
        r'\bmainstream media\b',
        r'\bthey don\'t want you to know\b'
    ]
    
    found_phrases = []
    text_lower = text.lower()
    
    for pattern in fake_indicators:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        found_phrases.extend(matches)
    
    # Remove duplicates and limit results
    unique_phrases = list(set(found_phrases))
    return unique_phrases[:max_phrases]


def get_confidence_interpretation(confidence):
    """Get human-readable interpretation of confidence score.
    
    Args:
        confidence (float): Confidence score (0-1)
        
    Returns:
        dict: Confidence interpretation
    """
    if confidence >= 0.9:
        level = "very high"
        description = "The model is very confident in this prediction"
    elif confidence >= 0.8:
        level = "high"
        description = "The model is confident in this prediction"
    elif confidence >= 0.7:
        level = "medium-high"
        description = "The model is moderately confident in this prediction"
    elif confidence >= 0.6:
        level = "medium"
        description = "The model has moderate confidence in this prediction"
    elif confidence >= 0.5:
        level = "low-medium"
        description = "The model has low-medium confidence in this prediction"
    else:
        level = "low"
        description = "The model has low confidence in this prediction"
    
    return {
        'level': level,
        'description': description,
        'numerical_score': confidence,
        'percentage': round(confidence * 100, 1)
    }