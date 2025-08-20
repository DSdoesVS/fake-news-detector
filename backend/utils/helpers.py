"""
Utility functions for the Fake News Detector application
"""

import re
import string
import nltk
from textblob import TextBlob
import pandas as pd
import numpy as np

def clean_text(text):
    """
    Clean and normalize text data
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def remove_punctuation(text):
    """
    Remove punctuation from text
    """
    if not isinstance(text, str):
        return ""
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def get_text_stats(text):
    """
    Get basic statistics about text
    """
    if not isinstance(text, str):
        return {
            'length': 0,
            'word_count': 0,
            'sentence_count': 0,
            'avg_word_length': 0,
            'avg_sentence_length': 0
        }
    
    # Basic stats
    length = len(text)
    words = text.split()
    word_count = len(words)
    
    # Sentence count using TextBlob
    try:
        blob = TextBlob(text)
        sentence_count = len(blob.sentences)
    except:
        sentence_count = text.count('.') + text.count('!') + text.count('?')
    
    # Average word length
    avg_word_length = np.mean([len(word) for word in words]) if words else 0
    
    # Average sentence length
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    return {
        'length': length,
        'word_count': word_count,
        'sentence_count': sentence_count,
        'avg_word_length': round(avg_word_length, 2),
        'avg_sentence_length': round(avg_sentence_length, 2)
    }

def get_sentiment_score(text):
    """
    Get sentiment polarity and subjectivity using TextBlob
    """
    if not isinstance(text, str) or len(text.strip()) == 0:
        return {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'sentiment': 'neutral'
        }
    
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment label
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'sentiment': sentiment
        }
    except:
        return {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'sentiment': 'neutral'
        }

def validate_text_input(text, min_length=10, max_length=10000):
    """
    Validate text input for prediction
    """
    errors = []
    
    if not text:
        errors.append("Text is required")
        return False, errors
    
    if not isinstance(text, str):
        errors.append("Text must be a string")
        return False, errors
    
    text = text.strip()
    
    if len(text) < min_length:
        errors.append(f"Text must be at least {min_length} characters long")
    
    if len(text) > max_length:
        errors.append(f"Text must be no more than {max_length} characters long")
    
    # Check if text contains enough words
    words = text.split()
    if len(words) < 3:
        errors.append("Text must contain at least 3 words")
    
    return len(errors) == 0, errors

def format_prediction_response(prediction, confidence, text, additional_info=None):
    """
    Format prediction response for API
    """
    response = {
        'prediction': 'REAL' if prediction == 1 else 'FAKE',
        'confidence': float(confidence),
        'confidence_percentage': f"{confidence * 100:.2f}%",
        'prediction_label': prediction,
        'text_stats': get_text_stats(text),
        'sentiment_analysis': get_sentiment_score(text)
    }
    
    if additional_info:
        response.update(additional_info)
    
    return response

def log_prediction(text, prediction, confidence, timestamp=None):
    """
    Log prediction for monitoring and analysis
    """
    import datetime
    
    if timestamp is None:
        timestamp = datetime.datetime.now()
    
    log_entry = {
        'timestamp': timestamp.isoformat(),
        'text_length': len(text),
        'prediction': 'REAL' if prediction == 1 else 'FAKE',
        'confidence': float(confidence),
        'text_preview': text[:100] + '...' if len(text) > 100 else text
    }
    
    return log_entry
