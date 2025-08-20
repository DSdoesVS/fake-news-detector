#!/usr/bin/env python3
"""
Script to train the fake news detection model
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'backend'))

from backend.models.train_model import train_and_save_model

def main():
    print("=" * 50)
    print("FAKE NEWS DETECTOR - MODEL TRAINING")
    print("=" * 50)
    
    print("\nStarting model training process...")
    
    try:
        success = train_and_save_model()
        
        if success:
            print("\n" + "=" * 50)
            print("✅ MODEL TRAINING COMPLETED SUCCESSFULLY!")
            print("=" * 50)
            print("\nThe model has been saved and is ready to use.")
            print("You can now start the Flask API server with:")
            print("  python backend/app.py")
        else:
            print("\n" + "=" * 50)
            print("❌ MODEL TRAINING FAILED!")
            print("=" * 50)
            print("\nPlease check the error messages above.")
            return 1
            
    except Exception as e:
        print(f"\n❌ Training failed with error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
