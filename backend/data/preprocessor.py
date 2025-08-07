"""Text preprocessing utilities for the Fake News Detector."""

import re
import string
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

logger = logging.getLogger(__name__)


class TextPreprocessor:
    """Handles text preprocessing for news articles."""
    
    def __init__(self, download_nltk_data=True):
        """Initialize the text preprocessor.
        
        Args:
            download_nltk_data (bool): Whether to download required NLTK data
        """
        self.stemmer = PorterStemmer()
        
        if download_nltk_data:
            self._download_nltk_data()
        
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            logger.warning("NLTK stopwords not available, using basic English stopwords")
            self.stop_words = {
                'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
                'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
                'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
                'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
                'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
                'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
                'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after', 'above',
                'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                'further', 'then', 'once'
            }
    
    def _download_nltk_data(self):
        """Download required NLTK data."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logger.info("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            logger.info("Downloading NLTK stopwords...")
            nltk.download('stopwords', quiet=True)
    
    def clean_text(self, text):
        """Clean text by removing unwanted characters and formatting.
        
        Args:
            text (str): Raw text to clean
            
        Returns:
            str: Cleaned text
        """
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
        """Remove punctuation from text.
        
        Args:
            text (str): Text with punctuation
            
        Returns:
            str: Text without punctuation
        """
        # Keep alphanumeric characters and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text
    
    def tokenize_text(self, text):
        """Tokenize text into words.
        
        Args:
            text (str): Text to tokenize
            
        Returns:
            list: List of tokens
        """
        try:
            tokens = word_tokenize(text)
        except LookupError:
            # Fallback to simple split if NLTK tokenizer is not available
            tokens = text.split()
        
        return tokens
    
    def remove_stopwords(self, tokens):
        """Remove stopwords from token list.
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            list: Tokens with stopwords removed
        """
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def stem_tokens(self, tokens):
        """Apply stemming to tokens.
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            list: Stemmed tokens
        """
        return [self.stemmer.stem(token) for token in tokens]
    
    def filter_tokens(self, tokens, min_length=2):
        """Filter tokens by length and remove numeric-only tokens.
        
        Args:
            tokens (list): List of tokens
            min_length (int): Minimum token length
            
        Returns:
            list: Filtered tokens
        """
        filtered = []
        for token in tokens:
            # Keep tokens that are at least min_length and not purely numeric
            if len(token) >= min_length and not token.isdigit():
                filtered.append(token)
        
        return filtered
    
    def preprocess_text(self, text, remove_stopwords=True, apply_stemming=True):
        """Complete text preprocessing pipeline.
        
        Args:
            text (str): Raw text to preprocess
            remove_stopwords (bool): Whether to remove stopwords
            apply_stemming (bool): Whether to apply stemming
            
        Returns:
            str: Preprocessed text ready for vectorization
        """
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
        
        # Apply stemming if requested
        if apply_stemming:
            tokens = self.stem_tokens(tokens)
        
        # Join tokens back into text
        processed_text = ' '.join(tokens)
        
        return processed_text
    
    def preprocess_batch(self, texts, remove_stopwords=True, apply_stemming=True):
        """Preprocess a batch of texts.
        
        Args:
            texts (list): List of raw texts
            remove_stopwords (bool): Whether to remove stopwords
            apply_stemming (bool): Whether to apply stemming
            
        Returns:
            list: List of preprocessed texts
        """
        processed_texts = []
        for text in texts:
            processed = self.preprocess_text(text, remove_stopwords, apply_stemming)
            processed_texts.append(processed)
        
        return processed_texts
    
    def get_text_stats(self, text):
        """Get statistics about the text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Text statistics
        """
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