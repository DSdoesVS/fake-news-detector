#!/usr/bin/env python3
"""
Startup script for the Fake News Detector API
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Set environment variables
os.environ.setdefault('FLASK_APP', 'app.py')
os.environ.setdefault('FLASK_ENV', 'development')

from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 STARTING FAKE NEWS DETECTOR API SERVER")
    print("=" * 60)
    print(f"📡 Server will be available at: http://localhost:5000")
    print(f"📋 API Documentation: http://localhost:5000")
    print(f"🔍 Health Check: http://localhost:5000/health")
    print("=" * 60)
    print("\n🔄 Starting server...\n")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
