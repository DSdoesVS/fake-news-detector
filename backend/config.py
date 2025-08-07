"""Configuration settings for the Fake News Detector backend."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Model configuration
    MODEL_PATH = os.environ.get('MODEL_PATH') or 'models/trained_model.joblib'
    VECTORIZER_PATH = os.environ.get('VECTORIZER_PATH') or 'models/vectorizer.joblib'
    
    # Data configuration
    SAMPLE_DATA_PATH = os.environ.get('SAMPLE_DATA_PATH') or 'data/sample_data.csv'
    
    # CORS configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # API configuration
    API_PREFIX = '/api'
    MAX_TEXT_LENGTH = int(os.environ.get('MAX_TEXT_LENGTH', 10000))


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}