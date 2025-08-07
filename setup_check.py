#!/usr/bin/env python3
"""Setup validation script for the Fake News Detector project."""

import os
import sys
import subprocess
import json

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def check_node_version():
    """Check if Node.js version is 16+"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip().replace('v', '')
            major_version = int(version.split('.')[0])
            if major_version >= 16:
                print(f"✅ Node.js {version} - OK")
                return True
            else:
                print(f"❌ Node.js {version} - Requires Node.js 16+")
                return False
        else:
            print("❌ Node.js - Not installed")
            return False
    except FileNotFoundError:
        print("❌ Node.js - Not installed")
        return False

def check_project_structure():
    """Check if project structure is correct"""
    required_files = [
        'backend/app.py',
        'backend/config.py',
        'backend/requirements.txt',
        'frontend/package.json',
        'frontend/src/App.js',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if not missing_files:
        print("✅ Project structure - OK")
        return True
    else:
        print("❌ Project structure - Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False

def check_backend_dependencies():
    """Check if backend dependencies can be imported"""
    try:
        # Test basic Python functionality
        sys.path.append('backend')
        from models.mock_predictor import MockPredictor
        from utils.helpers import validate_text_input
        print("✅ Backend dependencies (mock) - OK")
        return True
    except ImportError as e:
        print(f"❌ Backend dependencies - Error: {e}")
        return False

def run_backend_test():
    """Run backend functionality test"""
    try:
        sys.path.append('backend')
        from models.mock_predictor import MockPredictor
        from utils.helpers import validate_text_input, format_prediction_response
        
        predictor = MockPredictor()
        test_text = "This is a test article to verify the system is working."
        
        # Test validation
        validation_error = validate_text_input(test_text, 10000)
        if validation_error:
            print(f"❌ Backend test - Validation failed: {validation_error}")
            return False
        
        # Test prediction
        prediction, confidence = predictor.predict(test_text)
        response = format_prediction_response(prediction, confidence, test_text)
        
        if 'prediction' in response and 'confidence' in response:
            print("✅ Backend functionality test - OK")
            return True
        else:
            print("❌ Backend functionality test - Invalid response format")
            return False
            
    except Exception as e:
        print(f"❌ Backend functionality test - Error: {e}")
        return False

def main():
    """Main validation function"""
    print("🔍 Fake News Detector - Setup Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Node.js Version", check_node_version),
        ("Project Structure", check_project_structure),
        ("Backend Dependencies", check_backend_dependencies),
        ("Backend Functionality", run_backend_test)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        if check_func():
            passed += 1
        else:
            print(f"   💡 Tip: Check README.md for setup instructions")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Your setup is ready.")
        print("\n🚀 Next steps:")
        print("   1. Install dependencies: cd backend && pip install -r requirements.txt")
        print("   2. Start backend: cd backend && python app.py")
        print("   3. Install frontend: cd frontend && npm install")
        print("   4. Start frontend: cd frontend && npm start")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("📖 See README.md for detailed setup instructions.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)