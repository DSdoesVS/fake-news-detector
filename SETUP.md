# 🚀 Quick Setup Guide

This guide will help you get the Fake News Detector application running on your system.

## 📋 Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)
- A web browser
- At least 2GB of RAM for model training

## 🛠️ Installation & Setup

### 1. Clone or Download the Project

If you haven't already, make sure you have the project files in your desired directory.

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 4. Prepare the Data

Make sure you have the following files in the `data/` directory:
- `Fake.csv.zip` - Contains fake news articles
- `True.csv.zip` - Contains real news articles

### 5. Train the Model

Before running the application, you need to train the machine learning model:

```bash
# Train the model (this may take a few minutes)
python train_model.py
```

This will:
- Extract and load the data from ZIP files
- Preprocess the text data
- Train a Logistic Regression model with TF-IDF features
- Save the trained model and vectorizer

### 6. Start the Backend API

```bash
# Navigate to backend directory
cd backend

# Start the Flask API server
python run_server.py
```

The API will be available at: `http://localhost:5000`

### 7. Open the Frontend

Open your web browser and navigate to:
```
file:///path/to/your/project/frontend/index.html
```

Or use a simple HTTP server:

```bash
# Navigate to frontend directory
cd frontend

# Start a simple HTTP server (Python 3)
python -m http.server 8080

# Then open: http://localhost:8080
```

## 🧪 Testing the Application

1. **Health Check**: Visit `http://localhost:5000/health` to ensure the API is running and the model is loaded.

2. **Web Interface**: Use the frontend to input news articles and get predictions.

3. **API Testing**: You can test the API directly using curl:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a sample news article text to analyze for authenticity."}'
```

## 📁 Project Structure

```
fake-news-detector/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── run_server.py         # Server startup script
│   ├── config.py             # Configuration settings
│   ├── models/
│   │   ├── train_model.py    # Model training script
│   │   ├── predictor.py      # Prediction logic
│   │   ├── fake_news_model.pkl    # Trained model (after training)
│   │   └── tfidf_vectorizer.pkl   # Trained vectorizer (after training)
│   ├── data/
│   │   └── preprocessor.py   # Text preprocessing utilities
│   └── utils/
│       └── helpers.py        # Utility functions
├── frontend/
│   ├── index.html           # Main web interface
│   ├── styles/
│   │   └── main.css        # Custom styles
│   └── js/
│       └── main.js         # Frontend JavaScript
├── data/
│   ├── Fake.csv.zip        # Fake news dataset
│   └── True.csv.zip        # Real news dataset
├── notebooks/
│   └── 01-model-development.ipynb  # Jupyter notebook for development
├── train_model.py          # Model training script
├── requirements.txt        # Python dependencies
├── .env                   # Environment configuration
└── README.md             # Project documentation
```

## 🔧 Troubleshooting

### Common Issues:

1. **ModuleNotFoundError**: Make sure you've activated the virtual environment and installed all dependencies.

2. **Model not found**: Run `python train_model.py` to train and save the model.

3. **API connection failed**: Ensure the backend server is running on port 5000.

4. **CORS errors**: The backend is configured to allow requests from common development ports.

5. **Memory issues**: Model training requires sufficient RAM. Close other applications if needed.

### Performance Tips:

- **Model Training**: First-time training may take 5-10 minutes depending on your system.
- **Prediction Speed**: Once loaded, predictions are typically very fast (< 1 second).
- **Browser Compatibility**: The frontend works best in modern browsers (Chrome, Firefox, Safari, Edge).

## 🎯 Usage Examples

### Web Interface:
1. Paste a news article into the text area
2. Click "Analyze Article"
3. View the prediction result with confidence score

### API Usage:
```python
import requests

url = "http://localhost:5000/predict"
data = {
    "text": "Your news article text here..."
}

response = requests.post(url, json=data)
result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence_percentage']}")
```

## 🚀 Next Steps

- Try different types of news articles to test the model
- Explore the Jupyter notebook for model development insights
- Customize the frontend design to match your preferences
- Consider fine-tuning the model with additional data

## 📞 Support

If you encounter any issues:
1. Check that all dependencies are installed correctly
2. Ensure the data files are in the correct location
3. Verify that the model training completed successfully
4. Check the console/terminal for error messages

Happy fake news detecting! 🕵️‍♂️
