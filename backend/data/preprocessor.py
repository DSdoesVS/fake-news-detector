"""
Data preprocessing utilities for the Fake News Detector
"""

import pandas as pd
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class TextPreprocessor:
    """
    Text preprocessing class for fake news detection
    """
    
    def __init__(self, remove_stopwords=True, use_stemming=False):
        self.remove_stopwords = remove_stopwords
        self.use_stemming = use_stemming
        self.stemmer = PorterStemmer() if use_stemming else None
        
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
    
    def clean_text(self, text):
        """
        Clean text by removing unwanted characters and formatting
        """
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def remove_punctuation(self, text):
        """
        Remove punctuation from text
        """
        if not isinstance(text, str):
            return ""
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        return text
    
    def tokenize_and_filter(self, text):
        """
        Tokenize text and apply filtering (stopwords, stemming)
        """
        if not isinstance(text, str) or len(text.strip()) == 0:
            return []
        
        try:
            # Tokenize
            tokens = word_tokenize(text)
            
            # Remove stopwords
            if self.remove_stopwords:
                tokens = [token for token in tokens if token.lower() not in self.stop_words]
            
            # Apply stemming
            if self.use_stemming and self.stemmer:
                tokens = [self.stemmer.stem(token) for token in tokens]
            
            # Filter out short tokens
            tokens = [token for token in tokens if len(token) > 2]
            
            return tokens
        except:
            return []
    
    def preprocess(self, text):
        """
        Full preprocessing pipeline
        """
        # Clean text
        text = self.clean_text(text)
        
        # Remove punctuation
        text = self.remove_punctuation(text)
        
        # Tokenize and filter
        tokens = self.tokenize_and_filter(text)
        
        # Join tokens back to string
        return ' '.join(tokens)
    
    def preprocess_batch(self, texts):
        """
        Preprocess a batch of texts
        """
        return [self.preprocess(text) for text in texts]

class DataLoader:
    """
    Data loading and preparation class
    """
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.preprocessor = TextPreprocessor()
    
    def load_csv_data(self, fake_file='Fake.csv', true_file='True.csv'):
        """
        Load fake and true news data from CSV files
        """
        import os
        
        fake_path = os.path.join(self.data_dir, fake_file)
        true_path = os.path.join(self.data_dir, true_file)
        
        try:
            # Load fake news data
            if os.path.exists(fake_path):
                fake_df = pd.read_csv(fake_path)
                fake_df['label'] = 0  # Fake news
            else:
                print(f"Fake news file not found: {fake_path}")
                fake_df = pd.DataFrame()
            
            # Load true news data
            if os.path.exists(true_path):
                true_df = pd.read_csv(true_path)
                true_df['label'] = 1  # Real news
            else:
                print(f"True news file not found: {true_path}")
                true_df = pd.DataFrame()
            
            # Combine datasets
            if not fake_df.empty and not true_df.empty:
                df = pd.concat([fake_df, true_df], ignore_index=True)
                return df
            elif not fake_df.empty:
                return fake_df
            elif not true_df.empty:
                return true_df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return pd.DataFrame()
    
    def prepare_text_data(self, df):
        """
        Prepare text data for model training
        """
        if df.empty:
            return pd.DataFrame()
        
        # Combine title and text if both exist
        if 'title' in df.columns and 'text' in df.columns:
            df['content'] = df['title'].fillna('') + ' ' + df['text'].fillna('')
        elif 'text' in df.columns:
            df['content'] = df['text'].fillna('')
        elif 'title' in df.columns:
            df['content'] = df['title'].fillna('')
        else:
            print("No suitable text column found!")
            return pd.DataFrame()
        
        # Preprocess content
        df['processed_content'] = df['content'].apply(self.preprocessor.preprocess)
        
        # Remove empty content
        df = df[df['processed_content'].str.len() > 0]
        
        return df
    
    def get_statistics(self, df):
        """
        Get dataset statistics
        """
        if df.empty:
            return {}
        
        stats = {
            'total_articles': len(df),
            'fake_articles': len(df[df['label'] == 0]) if 'label' in df.columns else 0,
            'real_articles': len(df[df['label'] == 1]) if 'label' in df.columns else 0,
        }
        
        if 'content' in df.columns:
            stats['avg_content_length'] = df['content'].str.len().mean()
            stats['max_content_length'] = df['content'].str.len().max()
            stats['min_content_length'] = df['content'].str.len().min()
        
        if 'processed_content' in df.columns:
            stats['avg_processed_length'] = df['processed_content'].str.len().mean()
        
        return stats

def create_sample_data():
    """
    Create sample data for testing purposes
    """
    sample_data = [
        {
            'title': 'Breaking: Major Scientific Discovery',
            'text': 'Scientists at a leading university have made a groundbreaking discovery that could change our understanding of physics.',
            'label': 1
        },
        {
            'title': 'Shocking: Celebrity Secret Revealed',
            'text': 'You won\'t believe what this celebrity did! Click here to find out the shocking truth that the media doesn\'t want you to know!',
            'label': 0
        },
        {
            'title': 'Economic Update: Market Analysis',
            'text': 'The stock market showed mixed results today as investors weighed economic indicators and corporate earnings reports.',
            'label': 1
        },
        {
            'title': 'Miracle Cure: Doctors Hate This Trick',
            'text': 'This one weird trick will cure everything! Big pharma doesn\'t want you to know about this amazing discovery!',
            'label': 0
        }
    ]
    
    return pd.DataFrame(sample_data)
