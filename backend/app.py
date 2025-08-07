"""Main Flask application for the Fake News Detector."""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
from utils.helpers import validate_text_input, format_prediction_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """Create and configure the Flask application."""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize the predictor
    try:
        # Try to import the real predictor first
        from models.predictor import FakeNewsPredictor
        predictor = FakeNewsPredictor(
            model_path=app.config['MODEL_PATH'],
            vectorizer_path=app.config['VECTORIZER_PATH']
        )
        app.predictor = predictor
        logger.info("Real Fake News Predictor initialized successfully")
    except (ImportError, FileNotFoundError, Exception) as e:
        logger.warning(f"Could not initialize real predictor: {e}")
        try:
            # Fall back to mock predictor for testing
            from models.mock_predictor import MockPredictor
            predictor = MockPredictor(
                model_path=app.config['MODEL_PATH'],
                vectorizer_path=app.config['VECTORIZER_PATH']
            )
            app.predictor = predictor
            logger.info("Mock predictor initialized for testing")
        except Exception as e:
            logger.error(f"Could not initialize any predictor: {e}")
            app.predictor = None
    
    # Health check endpoint
    @app.route(app.config['API_PREFIX'] + '/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        status = {
            'status': 'healthy',
            'model_loaded': app.predictor is not None,
            'model_type': type(app.predictor).__name__ if app.predictor else None
        }
        return jsonify(status)
    
    # Prediction endpoint
    @app.route(app.config['API_PREFIX'] + '/predict', methods=['POST'])
    def predict():
        """Predict if a news article is fake or real."""
        try:
            # Validate request
            if not request.json or 'text' not in request.json:
                return jsonify({
                    'error': 'Invalid request. Please provide text in JSON format.'
                }), 400
            
            text = request.json['text']
            
            # Validate text input
            validation_error = validate_text_input(text, app.config['MAX_TEXT_LENGTH'])
            if validation_error:
                return jsonify({'error': validation_error}), 400
            
            # Check if predictor is available
            if app.predictor is None:
                return jsonify({
                    'error': 'Model not available. Please check server configuration.'
                }), 500
            
            # Make prediction
            prediction, confidence = app.predictor.predict(text)
            
            # Format response
            response = format_prediction_response(prediction, confidence, text)
            
            logger.info(f"Prediction made: {prediction} (confidence: {confidence:.2f})")
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return jsonify({
                'error': 'An error occurred while processing your request.'
            }), 500
    
    # Model info endpoint
    @app.route(app.config['API_PREFIX'] + '/model-info', methods=['GET'])
    def model_info():
        """Get information about the loaded model."""
        if app.predictor is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        info = app.predictor.get_model_info()
        return jsonify(info)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting Flask application on {host}:{port}")
    app.run(host=host, port=port, debug=app.config['DEBUG'])