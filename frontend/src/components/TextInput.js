import React, { useState } from 'react';

const TextInput = ({ onAnalyze, isLoading }) => {
  const [text, setText] = useState('');
  const [error, setError] = useState('');
  
  const maxLength = 10000;
  const minLength = 10;
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validation
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }
    
    if (text.length < minLength) {
      setError(`Text must be at least ${minLength} characters long`);
      return;
    }
    
    if (text.length > maxLength) {
      setError(`Text must be less than ${maxLength} characters`);
      return;
    }
    
    setError('');
    onAnalyze(text);
  };
  
  const handleTextChange = (e) => {
    setText(e.target.value);
    if (error) setError('');
  };
  
  const getCharCounterClass = () => {
    const ratio = text.length / maxLength;
    if (ratio > 0.9) return 'char-counter danger';
    if (ratio > 0.7) return 'char-counter warning';
    return 'char-counter';
  };
  
  return (
    <div className="card input-card">
      <div className="card-body p-4">
        <h5 className="card-title mb-3">📝 Enter News Article Text</h5>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <textarea
              className="form-control text-input"
              rows="8"
              placeholder="Paste or type the news article text you want to analyze here..."
              value={text}
              onChange={handleTextChange}
              disabled={isLoading}
              maxLength={maxLength}
            />
            <div className={getCharCounterClass()}>
              {text.length} / {maxLength} characters
            </div>
          </div>
          
          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}
          
          <div className="d-grid gap-2">
            <button
              type="submit"
              className="btn btn-primary btn-lg analyze-btn"
              disabled={isLoading || !text.trim()}
            >
              {isLoading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" />
                  Analyzing...
                </>
              ) : (
                <>
                  🔍 Analyze Article
                </>
              )}
            </button>
          </div>
        </form>
        
        <div className="mt-3">
          <small className="text-muted">
            💡 <strong>Tip:</strong> Paste a complete news article for best results. 
            The AI model analyzes language patterns, structure, and content to determine authenticity.
          </small>
        </div>
      </div>
    </div>
  );
};

export default TextInput;