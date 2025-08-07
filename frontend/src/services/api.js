import axios from 'axios';

// Base API URL - will use proxy in development
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging (development only)
if (process.env.NODE_ENV === 'development') {
  api.interceptors.request.use((config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  });
}

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * Check if the backend API is healthy
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    throw new Error('Backend service unavailable');
  }
};

/**
 * Predict if a news article is fake or real
 * @param {string} text - The news article text to analyze
 * @returns {Promise<Object>} Prediction result
 */
export const predictNews = async (text) => {
  try {
    if (!text || typeof text !== 'string') {
      throw new Error('Valid text is required for prediction');
    }
    
    const response = await api.post('/api/predict', {
      text: text.trim()
    });
    
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      if (status === 400) {
        throw new Error(data.error || 'Invalid input provided');
      } else if (status === 500) {
        throw new Error(data.error || 'Server error occurred');
      } else {
        throw new Error(`Request failed with status ${status}`);
      }
    } else if (error.request) {
      // Request made but no response received
      throw new Error('No response from server. Please check your connection.');
    } else {
      // Other errors
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
};

/**
 * Get information about the loaded model
 * @returns {Promise<Object>} Model information
 */
export const getModelInfo = async () => {
  try {
    const response = await api.get('/api/model-info');
    return response.data;
  } catch (error) {
    throw new Error('Could not retrieve model information');
  }
};

/**
 * Batch prediction for multiple texts (if backend supports it)
 * @param {Array<string>} texts - Array of news article texts
 * @returns {Promise<Array>} Array of prediction results
 */
export const predictNewsBatch = async (texts) => {
  try {
    if (!Array.isArray(texts) || texts.length === 0) {
      throw new Error('Valid array of texts is required');
    }
    
    const response = await api.post('/api/predict-batch', {
      texts: texts.map(text => text.trim())
    });
    
    return response.data;
  } catch (error) {
    if (error.response?.status === 404) {
      throw new Error('Batch prediction not supported by this version');
    }
    throw new Error(error.response?.data?.error || 'Batch prediction failed');
  }
};

/**
 * Utility function to validate text before sending to API
 * @param {string} text - Text to validate
 * @returns {Object} Validation result with isValid and error
 */
export const validateText = (text) => {
  if (!text || typeof text !== 'string') {
    return { isValid: false, error: 'Text is required' };
  }
  
  const trimmedText = text.trim();
  
  if (trimmedText.length < 10) {
    return { isValid: false, error: 'Text must be at least 10 characters long' };
  }
  
  if (trimmedText.length > 10000) {
    return { isValid: false, error: 'Text must be less than 10,000 characters' };
  }
  
  // Check if text contains mostly non-alphabetic characters
  const alphaCount = (trimmedText.match(/[a-zA-Z]/g) || []).length;
  const alphaRatio = alphaCount / trimmedText.length;
  
  if (alphaRatio < 0.3) {
    return { isValid: false, error: 'Text must contain at least 30% alphabetic characters' };
  }
  
  return { isValid: true, error: null };
};

/**
 * Utility function to format error messages for user display
 * @param {Error} error - Error object
 * @returns {string} User-friendly error message
 */
export const formatErrorMessage = (error) => {
  if (error.message) {
    return error.message;
  }
  
  if (typeof error === 'string') {
    return error;
  }
  
  return 'An unexpected error occurred. Please try again.';
};

/**
 * Test the API connection with a sample prediction
 * @returns {Promise<boolean>} True if API is working
 */
export const testConnection = async () => {
  try {
    await checkHealth();
    
    // Try a simple prediction with sample text
    const sampleText = "This is a test article to check if the API is working properly.";
    await predictNews(sampleText);
    
    return true;
  } catch (error) {
    console.error('API connection test failed:', error);
    return false;
  }
};

export default api;