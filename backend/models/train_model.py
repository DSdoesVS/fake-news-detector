"""
Model training pipeline for Fake News Detector
"""

import pandas as pd
import numpy as np
import re
import pickle
import os
import zipfile
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

def extract_data():
    """
    Extract and load data from zip files
    """
    # Get the project root directory (two levels up from current file)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(project_root, 'data')
    
    fake_zip = os.path.join(data_dir, 'Fake.csv.zip')
    true_zip = os.path.join(data_dir, 'True.csv.zip')
    
    # Extract fake news data
    if os.path.exists(fake_zip):
        with zipfile.ZipFile(fake_zip, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        fake_df = pd.read_csv(os.path.join(data_dir, 'Fake.csv'))
        fake_df['label'] = 0  # Fake news
    else:
        print("Fake.csv.zip not found!")
        return None
    
    # Extract true news data
    if os.path.exists(true_zip):
        with zipfile.ZipFile(true_zip, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        true_df = pd.read_csv(os.path.join(data_dir, 'True.csv'))
        true_df['label'] = 1  # Real news
    else:
        print("True.csv.zip not found!")
        return None
    
    # Combine datasets
    df = pd.concat([fake_df, true_df], ignore_index=True)
    
    return df

def preprocess_text(text):
    """
    Preprocess text for machine learning model
    """
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove punctuation and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def train_and_save_model():
    """
    Train the fake news detection model and save it
    """
    print("Starting model training...")
    
    # Load and extract data
    print("Loading data...")
    df = extract_data()
    
    if df is None:
        print("Failed to load data!")
        return False
    
    print(f"Loaded {len(df)} articles")
    print(f"Fake news articles: {len(df[df['label'] == 0])}")
    print(f"Real news articles: {len(df[df['label'] == 1])}")
    
    # Combine title and text for better feature extraction
    if 'title' in df.columns and 'text' in df.columns:
        df['content'] = df['title'].fillna('') + ' ' + df['text'].fillna('')
    elif 'text' in df.columns:
        df['content'] = df['text'].fillna('')
    elif 'title' in df.columns:
        df['content'] = df['title'].fillna('')
    else:
        print("No suitable text column found!")
        return False
    
    # Preprocess text
    print("Preprocessing text...")
    df['processed_content'] = df['content'].apply(preprocess_text)
    
    # Remove empty content
    df = df[df['processed_content'].str.len() > 0]
    
    print(f"After preprocessing: {len(df)} articles")
    
    # Prepare features and labels
    X = df['processed_content']
    y = df['label']
    
    # Split data
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set: {len(X_train)} articles")
    print(f"Test set: {len(X_test)} articles")
    
    # Vectorize text using TF-IDF
    print("Vectorizing text...")
    vectorizer = TfidfVectorizer(
        max_features=10000,
        stop_words='english',
        ngram_range=(1, 2),
        max_df=0.95,
        min_df=2
    )
    
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    
    # Train model
    print("Training model...")
    model = LogisticRegression(
        random_state=42,
        max_iter=1000,
        C=1.0
    )
    
    model.fit(X_train_vectorized, y_train)
    
    # Evaluate model
    print("Evaluating model...")
    y_pred = model.predict(X_test_vectorized)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Fake', 'Real']))
    
    # Create models directory if it doesn't exist
    models_dir = os.path.dirname(__file__)
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    
    # Save model and vectorizer
    print("Saving model...")
    model_path = os.path.join(models_dir, 'fake_news_model.pkl')
    vectorizer_path = os.path.join(models_dir, 'tfidf_vectorizer.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print(f"Model saved to: {model_path}")
    print(f"Vectorizer saved to: {vectorizer_path}")
    
    return True

if __name__ == "__main__":
    train_and_save_model()
