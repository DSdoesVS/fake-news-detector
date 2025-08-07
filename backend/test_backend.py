#!/usr/bin/env python3
"""Simple test script to verify the backend logic without Flask dependencies."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.mock_predictor import MockPredictor
from utils.helpers import validate_text_input, format_prediction_response


def test_backend():
    """Test the backend logic without Flask."""
    print("Testing Fake News Detector Backend...")
    
    # Initialize predictor
    predictor = MockPredictor()
    print(f"Predictor initialized: {predictor.is_loaded()}")
    
    # Test model info
    model_info = predictor.get_model_info()
    print(f"Model info: {model_info}")
    
    # Test cases
    test_cases = [
        {
            "name": "Real News",
            "text": "Scientists at MIT have developed a revolutionary new battery technology that could power electric vehicles for over 1000 miles on a single charge. The breakthrough involves a new lithium-metal composite that dramatically increases energy density while maintaining safety standards."
        },
        {
            "name": "Fake News",
            "text": "BREAKING: Government officials confirm alien contact established last week! Secret documents leaked show ongoing negotiations with extraterrestrial beings from Zeta Reticuli system. Military sources refuse to comment on the shocking revelations."
        },
        {
            "name": "Short Text (should fail validation)",
            "text": "Short"
        },
        {
            "name": "Long Text (should fail validation)",
            "text": "A" * 10001
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- Testing: {test_case['name']} ---")
        text = test_case['text']
        
        # Validate input
        validation_error = validate_text_input(text, 10000)
        if validation_error:
            print(f"Validation error: {validation_error}")
            continue
        
        # Make prediction
        try:
            prediction, confidence = predictor.predict(text)
            response = format_prediction_response(prediction, confidence, text)
            
            print(f"Prediction: {prediction}")
            print(f"Confidence: {confidence:.4f}")
            print(f"Response: {response}")
        except Exception as e:
            print(f"Prediction error: {e}")
    
    print("\nBackend testing completed!")


if __name__ == '__main__':
    test_backend()