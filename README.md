# 🕵️ Fake News Detector

A full-stack machine learning application that analyzes news articles to detect potential misinformation using natural language processing and classification algorithms.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![React](https://img.shields.io/badge/react-v18.2+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Features

- **Real-time Analysis**: Instantly analyze news articles for authenticity
- **Machine Learning Pipeline**: TF-IDF vectorization with Logistic Regression
- **Interactive Web Interface**: Clean, responsive React frontend
- **RESTful API**: Flask backend with prediction endpoints
- **Confidence Scoring**: Get prediction confidence levels
- **Extensible Architecture**: Ready for advanced ML models integration

## 🏗️ Project Structure

```
fake-news-detector/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── models/
│   │   ├── train_model.py     # Model training pipeline
│   │   └── predictor.py       # Prediction logic
│   ├── data/
│   │   ├── preprocessor.py    # Text preprocessing
│   │   └── sample_data.csv    # Sample dataset
│   ├── utils/
│   │   └── helpers.py         # Utility functions
│   ├── requirements.txt       # Python dependencies
│   └── config.py             # Configuration
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API communication
│   │   └── styles/           # CSS styling
│   └── package.json
├── README.md
├── .gitignore
└── docker-compose.yml
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask
- **ML Libraries**: scikit-learn, NLTK, pandas
- **Model**: TF-IDF + Logistic Regression
- **Data Processing**: NumPy, joblib

### Frontend
- **Framework**: React 18
- **Styling**: Bootstrap 5
- **HTTP Client**: Axios
- **Build Tool**: Create React App

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/DSdoesVS/fake-news-detector.git
cd fake-news-detector
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Train the model (first time only)
python models/train_model.py

# Start the Flask server
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

The frontend will run on `http://localhost:3000`

## 📡 API Documentation

### Base URL: `http://localhost:5000`

### Endpoints

#### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Fake News Detector API is running"
}
```

#### Predict News Authenticity
```http
POST /api/predict
Content-Type: application/json

{
  "text": "Your news article text here..."
}
```

**Response:**
```json
{
  "prediction": "fake",
  "confidence": 0.85,
  "processed_text": "cleaned article text...",
  "timestamp": "2025-08-07T09:47:39Z"
}
```

**Prediction Values:**
- `"real"`: Article appears to be authentic
- `"fake"`: Article appears to be misinformation

## 🧠 Machine Learning Pipeline

### 1. Data Preprocessing
- Text normalization and cleaning
- Stop word removal
- Tokenization using NLTK
- Feature extraction with TF-IDF

### 2. Model Training
- **Algorithm**: Logistic Regression
- **Features**: TF-IDF vectors (max 5000 features)
- **Evaluation**: Cross-validation with accuracy, precision, recall

### 3. Prediction Pipeline
- Real-time text preprocessing
- Feature vectorization
- Model inference with confidence scoring

## 🎨 Frontend Features

### Components
- **TextInput**: News article input with character count
- **ResultDisplay**: Prediction results with confidence visualization
- **Header**: Application branding and navigation
- **LoadingSpinner**: User feedback during API calls

### User Experience
- Responsive design for all devices
- Real-time validation and feedback
- Error handling with user-friendly messages
- Confidence score visualization

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
```

### Individual Container Builds
```bash
# Backend
cd backend
docker build -t fake-news-detector-backend .

# Frontend
cd frontend
docker build -t fake-news-detector-frontend .
```

## ☁️ Cloud Deployment

### Heroku (Backend)
```bash
# Install Heroku CLI and login
heroku create your-app-name-backend
git subtree push --prefix backend heroku main
```

### Vercel (Frontend)
```bash
# Install Vercel CLI
npm i -g vercel
cd frontend
vercel --prod
```

### Environment Variables
Create `.env` files for configuration:

**Backend (.env):**
```
FLASK_ENV=production
MODEL_PATH=models/trained_model.joblib
CORS_ORIGINS=https://your-frontend-domain.com
```

**Frontend (.env):**
```
REACT_APP_API_URL=https://your-backend-api.herokuapp.com
```

## 🔬 Model Performance

Current baseline model metrics:
- **Accuracy**: ~85%
- **Precision**: ~83%
- **Recall**: ~87%
- **F1-Score**: ~85%

*Note: Performance may vary based on training data quality and size.*

## 🚀 Future Enhancements

### Advanced ML Models
- [ ] BERT/DistilBERT integration
- [ ] Ensemble methods
- [ ] Real-time model updates
- [ ] Multi-language support

### Features
- [ ] User authentication and history
- [ ] Batch article processing
- [ ] News source credibility scoring
- [ ] Social media integration
- [ ] Browser extension

### Technical Improvements
- [ ] Model A/B testing framework
- [ ] Automated retraining pipeline
- [ ] Performance monitoring
- [ ] Caching layer for predictions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript code
- Add tests for new features
- Update documentation as needed

## 📊 Dataset Information

The project includes sample datasets for training and testing. For production use, consider:

- **Kaggle Fake News Dataset**
- **LIAR Dataset**
- **FakeNewsNet**
- **Custom scraped news articles**

### Data Format
```csv
title,text,label
"Article Title","Article content...","fake"
"Another Title","More content...","real"
```

## 🐛 Troubleshooting

### Common Issues

**Backend Issues:**
```bash
# NLTK data missing
python -c "import nltk; nltk.download('all')"

# Port already in use
lsof -ti:5000 | xargs kill -9
```

**Frontend Issues:**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Support
- Create an issue for bugs or feature requests
- Check existing issues before posting
- Provide detailed error messages and system info

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**DSdoesVS**
- GitHub: [@DSdoesVS](https://github.com/DSdoesVS)

## 🙏 Acknowledgments

- scikit-learn team for excellent ML tools
- React community for frontend best practices
- NLTK contributors for NLP utilities
- Open source fake news datasets

---

⭐ **Star this repository if you found it helpful!**

🚀 **Ready to detect fake news? Start with the Quick Start guide above!**
