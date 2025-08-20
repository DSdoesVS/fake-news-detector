"""
Configuration settings for the Fake News Detector application
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # API settings
    API_HOST = os.environ.get('API_HOST', '0.0.0.0')
    API_PORT = int(os.environ.get('API_PORT', 5000))
    
    # Model settings
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'fake_news_model.pkl')
    VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'models', 'tfidf_vectorizer.pkl')
    
    # Data settings
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    # Text preprocessing settings
    MAX_FEATURES = 10000
    NGRAM_RANGE = (1, 2)
    MAX_DF = 0.95
    MIN_DF = 2
    
    # Model training settings
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    MAX_ITER = 1000
    REGULARIZATION_C = 1.0

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
