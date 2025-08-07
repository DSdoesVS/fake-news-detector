import React from 'react';

const ResultDisplay = ({ result, error }) => {
  if (error) {
    return (
      <div className="card prediction-card fade-in">
        <div className="card-body p-4">
          <div className="error-message">
            <h5 className="mb-2">❌ Analysis Error</h5>
            <p className="mb-0">{error}</p>
          </div>
        </div>
      </div>
    );
  }
  
  if (!result) {
    return null;
  }
  
  const { prediction, confidence, confidence_percentage, confidence_level, text_stats, timestamp } = result;
  const isFake = prediction === 'fake';
  
  const getConfidenceColor = () => {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.6) return 'warning';
    return 'danger';
  };
  
  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };
  
  return (
    <div className="card prediction-card fade-in">
      <div className="card-body p-4">
        <div className={`result-${prediction}`}>
          <div className="row align-items-center">
            <div className="col-md-8">
              <h4 className="mb-2">
                {isFake ? '🚨 Likely FAKE News' : '✅ Likely REAL News'}
              </h4>
              <p className="mb-3">
                {isFake 
                  ? 'This article shows characteristics commonly found in fake news content.'
                  : 'This article appears to be authentic news content.'
                }
              </p>
            </div>
            <div className="col-md-4 text-center">
              <div className="display-6 mb-2">{confidence_percentage}%</div>
              <small>Confidence</small>
            </div>
          </div>
          
          <div className="confidence-bar">
            <div 
              className="confidence-fill" 
              style={{ width: `${confidence_percentage}%` }}
            />
          </div>
          
          <div className="prediction-details">
            <div className="detail-item">
              <span className="detail-label">Prediction:</span>
              <span className="detail-value">{prediction.toUpperCase()}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Confidence Level:</span>
              <span className="detail-value">{confidence_level.toUpperCase()}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Confidence Score:</span>
              <span className="detail-value">{confidence.toFixed(4)}</span>
            </div>
          </div>
        </div>
        
        {text_stats && (
          <div className="mt-4">
            <h6 className="mb-3">📊 Text Analysis</h6>
            <div className="row">
              <div className="col-md-4">
                <div className="text-center p-3 bg-light rounded">
                  <div className="h5 mb-1">{text_stats.word_count}</div>
                  <small className="text-muted">Words</small>
                </div>
              </div>
              <div className="col-md-4">
                <div className="text-center p-3 bg-light rounded">
                  <div className="h5 mb-1">{text_stats.character_count}</div>
                  <small className="text-muted">Characters</small>
                </div>
              </div>
              <div className="col-md-4">
                <div className="text-center p-3 bg-light rounded">
                  <div className="h5 mb-1">{text_stats.sentence_count}</div>
                  <small className="text-muted">Sentences</small>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div className="mt-4 pt-3 border-top">
          <div className="row">
            <div className="col-md-6">
              <small className="text-muted">
                <strong>Analysis completed:</strong> {formatTimestamp(timestamp)}
              </small>
            </div>
            <div className="col-md-6 text-md-end">
              <small className="text-muted">
                Powered by Machine Learning & NLP
              </small>
            </div>
          </div>
        </div>
        
        <div className="mt-3">
          <div className="alert alert-info mb-0">
            <small>
              <strong>📌 Disclaimer:</strong> This is an AI prediction based on language patterns. 
              Always verify important news through multiple reliable sources.
            </small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;