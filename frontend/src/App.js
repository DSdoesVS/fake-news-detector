import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import TextInput from './components/TextInput';
import ResultDisplay from './components/ResultDisplay';
import { predictNews, checkHealth, formatErrorMessage } from './services/api';

function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState('unknown'); // 'healthy', 'unhealthy', 'unknown'

  // Check API health on component mount
  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        await checkHealth();
        setApiStatus('healthy');
      } catch (error) {
        setApiStatus('unhealthy');
        console.warn('API health check failed:', error.message);
      }
    };

    checkApiHealth();
  }, []);

  const handleAnalyze = async (text) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const prediction = await predictNews(text);
      setResult(prediction);
    } catch (error) {
      const errorMessage = formatErrorMessage(error);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const renderApiStatus = () => {
    if (apiStatus === 'unhealthy') {
      return (
        <div className="alert alert-warning" role="alert">
          <strong>⚠️ Backend Unavailable:</strong> The AI model is currently not available. 
          Please make sure the backend server is running.
        </div>
      );
    }
    return null;
  };

  return (
    <div className="app">
      <div className="container main-container">
        <div className="row justify-content-center">
          <div className="col-lg-8 col-xl-7">
            <Header />
            
            {renderApiStatus()}
            
            <div className="mb-4">
              <TextInput 
                onAnalyze={handleAnalyze} 
                isLoading={isLoading}
              />
            </div>
            
            {(result || error) && (
              <div className="mb-4">
                <ResultDisplay 
                  result={result} 
                  error={error}
                />
              </div>
            )}
            
            {/* Sample Examples Section */}
            <div className="card input-card mt-4">
              <div className="card-body p-4">
                <h5 className="card-title mb-3">💡 Try These Examples</h5>
                
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <div className="card border-success">
                      <div className="card-header bg-success text-white">
                        <small><strong>✅ Real News Example</strong></small>
                      </div>
                      <div className="card-body">
                        <small className="text-muted">
                          "Scientists at MIT have developed a revolutionary new battery technology that could power electric vehicles for over 1000 miles on a single charge. The breakthrough involves a new lithium-metal composite that dramatically increases energy density while maintaining safety standards."
                        </small>
                        <button 
                          className="btn btn-outline-success btn-sm mt-2 w-100"
                          onClick={() => handleAnalyze("Scientists at MIT have developed a revolutionary new battery technology that could power electric vehicles for over 1000 miles on a single charge. The breakthrough involves a new lithium-metal composite that dramatically increases energy density while maintaining safety standards.")}
                          disabled={isLoading}
                        >
                          Test This Example
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <div className="col-md-6 mb-3">
                    <div className="card border-danger">
                      <div className="card-header bg-danger text-white">
                        <small><strong>🚨 Fake News Example</strong></small>
                      </div>
                      <div className="card-body">
                        <small className="text-muted">
                          "BREAKING: Government officials confirm alien contact established last week! Secret documents leaked show ongoing negotiations with extraterrestrial beings from Zeta Reticuli system. Military sources refuse to comment on the shocking revelations."
                        </small>
                        <button 
                          className="btn btn-outline-danger btn-sm mt-2 w-100"
                          onClick={() => handleAnalyze("BREAKING: Government officials confirm alien contact established last week! Secret documents leaked show ongoing negotiations with extraterrestrial beings from Zeta Reticuli system. Military sources refuse to comment on the shocking revelations.")}
                          disabled={isLoading}
                        >
                          Test This Example
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="text-center mt-3">
                  <small className="text-muted">
                    <strong>How it works:</strong> The AI analyzes language patterns, writing style, 
                    emotional triggers, and structural elements to determine authenticity.
                  </small>
                </div>
              </div>
            </div>
            
            {/* Footer */}
            <div className="app-footer">
              <p className="mb-2">
                <strong>Fake News Detector</strong> - AI-Powered News Authenticity Analysis
              </p>
              <p className="mb-0">
                <small>
                  Built with React, Flask, and Machine Learning • 
                  <a href="#" className="footer-link ms-1">Learn More</a>
                </small>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;