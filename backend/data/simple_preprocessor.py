"""Simple text preprocessing without external dependencies."""

import re
import string
import logging

logger = logging.getLogger(__name__)


class SimpleTextPreprocessor:
    """Simple text preprocessor that works without NLTK."""
    
    def __init__(self):
        """Initialize the simple text preprocessor."""
        # Basic English stop words
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have',
            'had', 'what', 'said', 'each', 'which', 'she', 'do', 'how', 'their',
            'if', 'up', 'out', 'many', 'then', 'them', 'these', 'so', 'some',
            'her', 'would', 'make', 'like', 'into', 'him', 'time', 'two', 'more',
            'go', 'no', 'way', 'could', 'my', 'than', 'first', 'been', 'call',
            'who', 'oil', 'sit', 'now', 'find', 'down', 'day', 'did', 'get',
            'come', 'made', 'may', 'part'
        }
    
    def clean_text(self, text):
        """Clean text by removing unwanted characters and formatting."""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def remove_punctuation(self, text):
        """Remove punctuation from text."""
        # Keep alphanumeric characters and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text
    
    def tokenize_text(self, text):
        """Simple tokenization by splitting on whitespace."""
        return text.split()
    
    def remove_stopwords(self, tokens):
        """Remove stopwords from token list."""
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def filter_tokens(self, tokens, min_length=2):
        """Filter tokens by length and remove numeric-only tokens."""
        filtered = []
        for token in tokens:
            # Keep tokens that are at least min_length and not purely numeric
            if len(token) >= min_length and not token.isdigit():
                filtered.append(token)
        
        return filtered
    
    def preprocess_text(self, text, remove_stopwords=True):
        """Complete text preprocessing pipeline."""
        if not text or not isinstance(text, str):
            return ""
        
        # Clean the text
        text = self.clean_text(text)
        
        # Remove punctuation
        text = self.remove_punctuation(text)
        
        # Tokenize
        tokens = self.tokenize_text(text)
        
        # Remove stopwords if requested
        if remove_stopwords:
            tokens = self.remove_stopwords(tokens)
        
        # Filter tokens
        tokens = self.filter_tokens(tokens)
        
        # Join tokens back into text
        processed_text = ' '.join(tokens)
        
        return processed_text
    
    def get_text_stats(self, text):
        """Get statistics about the text."""
        if not text or not isinstance(text, str):
            return {'error': 'Invalid text input'}
        
        # Original text stats
        original_word_count = len(text.split())
        original_char_count = len(text)
        
        # Preprocessed text stats
        processed_text = self.preprocess_text(text)
        processed_word_count = len(processed_text.split())
        processed_char_count = len(processed_text)
        
        return {
            'original': {
                'word_count': original_word_count,
                'character_count': original_char_count
            },
            'processed': {
                'word_count': processed_word_count,
                'character_count': processed_char_count
            },
            'reduction': {
                'word_reduction': original_word_count - processed_word_count,
                'char_reduction': original_char_count - processed_char_count
            }
        }