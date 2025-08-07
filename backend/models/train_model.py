"""Model training pipeline for the Fake News Detector."""

import os
import pandas as pd
import numpy as np
import joblib
import logging
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from data.preprocessor import TextPreprocessor

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Handles training of the fake news detection model."""
    
    def __init__(self, random_state=42):
        """Initialize the model trainer.
        
        Args:
            random_state (int): Random state for reproducibility
        """
        self.random_state = random_state
        self.vectorizer = None
        self.model = None
        self.preprocessor = TextPreprocessor()
        
    def load_data(self, data_path):
        """Load and preprocess training data.
        
        Args:
            data_path (str): Path to the CSV file containing training data
            
        Returns:
            tuple: (X, y) where X is text data and y is labels
        """
        try:
            df = pd.read_csv(data_path)
            
            # Ensure required columns exist
            if 'text' not in df.columns or 'label' not in df.columns:
                raise ValueError("Data must contain 'text' and 'label' columns")
            
            # Preprocess text data
            X = df['text'].apply(self.preprocessor.preprocess_text)
            y = df['label']
            
            # Convert labels to binary if needed (0 = real, 1 = fake)
            if y.dtype == 'object':
                y = y.map({'real': 0, 'fake': 1, 'REAL': 0, 'FAKE': 1})
            
            logger.info(f"Loaded {len(df)} samples from {data_path}")
            logger.info(f"Label distribution: {y.value_counts().to_dict()}")
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error loading data from {data_path}: {e}")
            raise
    
    def create_features(self, X_train, X_test=None):
        """Create TF-IDF features from text data.
        
        Args:
            X_train (pd.Series): Training text data
            X_test (pd.Series, optional): Test text data
            
        Returns:
            tuple: (X_train_tfidf, X_test_tfidf) or just X_train_tfidf if X_test is None
        """
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )
        
        # Fit and transform training data
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        
        if X_test is not None:
            X_test_tfidf = self.vectorizer.transform(X_test)
            return X_train_tfidf, X_test_tfidf
        
        return X_train_tfidf
    
    def train_model(self, X_train, y_train):
        """Train the logistic regression model.
        
        Args:
            X_train (scipy.sparse matrix): Training features
            y_train (pd.Series): Training labels
        """
        self.model = LogisticRegression(
            random_state=self.random_state,
            max_iter=1000,
            C=1.0
        )
        
        logger.info("Training logistic regression model...")
        self.model.fit(X_train, y_train)
        logger.info("Model training completed")
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate the trained model.
        
        Args:
            X_test (scipy.sparse matrix): Test features
            y_test (pd.Series): Test labels
            
        Returns:
            dict: Evaluation metrics
        """
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred)
        }
        
        logger.info("Model Evaluation Results:")
        for metric, value in metrics.items():
            logger.info(f"{metric.capitalize()}: {value:.4f}")
        
        # Detailed classification report
        logger.info("\nClassification Report:")
        logger.info(classification_report(y_test, y_pred, target_names=['Real', 'Fake']))
        
        return metrics
    
    def save_model(self, model_path, vectorizer_path):
        """Save the trained model and vectorizer.
        
        Args:
            model_path (str): Path to save the model
            vectorizer_path (str): Path to save the vectorizer
        """
        if self.model is None or self.vectorizer is None:
            raise ValueError("Model and vectorizer must be trained before saving")
        
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        os.makedirs(os.path.dirname(vectorizer_path), exist_ok=True)
        
        # Save model and vectorizer
        joblib.dump(self.model, model_path)
        joblib.dump(self.vectorizer, vectorizer_path)
        
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Vectorizer saved to {vectorizer_path}")
    
    def train_pipeline(self, data_path, model_path, vectorizer_path, test_size=0.2):
        """Complete training pipeline.
        
        Args:
            data_path (str): Path to training data
            model_path (str): Path to save the model
            vectorizer_path (str): Path to save the vectorizer
            test_size (float): Proportion of data to use for testing
            
        Returns:
            dict: Training results including metrics
        """
        logger.info("Starting training pipeline...")
        
        # Load data
        X, y = self.load_data(data_path)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        # Create features
        X_train_tfidf, X_test_tfidf = self.create_features(X_train, X_test)
        
        # Train model
        self.train_model(X_train_tfidf, y_train)
        
        # Evaluate model
        metrics = self.evaluate_model(X_test_tfidf, y_test)
        
        # Save model
        self.save_model(model_path, vectorizer_path)
        
        results = {
            'metrics': metrics,
            'total_samples': len(X),
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
        
        logger.info("Training pipeline completed successfully")
        return results


def main():
    """Main function to run model training."""
    trainer = ModelTrainer()
    
    # Set paths
    data_path = 'data/sample_data.csv'
    model_path = 'models/trained_model.joblib'
    vectorizer_path = 'models/vectorizer.joblib'
    
    try:
        results = trainer.train_pipeline(data_path, model_path, vectorizer_path)
        print("Training completed successfully!")
        print(f"Final metrics: {results['metrics']}")
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise


if __name__ == '__main__':
    main()