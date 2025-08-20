// Main JavaScript for Fake News Detector Frontend

// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const analysisForm = document.getElementById('analysis-form');
const newsTextArea = document.getElementById('news-text');
const analyzeBtn = document.getElementById('analyze-btn');
const loadingSpinner = document.getElementById('loading-spinner');
const statusText = document.getElementById('status-text');
const statusIndicator = document.getElementById('status-indicator');
const resultsSection = document.getElementById('results-section');
const resultsContent = document.getElementById('results-content');
const charCount = document.getElementById('char-count');

// State
let isAnalyzing = false;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Check API health
    checkApiHealth();
    
    // Set up event listeners
    setupEventListeners();
    
    // Update character count
    updateCharacterCount();
}

function setupEventListeners() {
    // Form submission
    analysisForm.addEventListener('submit', handleFormSubmit);
    
    // Character count update
    newsTextArea.addEventListener('input', updateCharacterCount);
    
    // Real-time validation
    newsTextArea.addEventListener('input', validateInput);
}

function updateCharacterCount() {
    const text = newsTextArea.value;
    charCount.textContent = text.length;
    
    // Update color based on length
    if (text.length < 10) {
        charCount.style.color = '#dc3545';
    } else if (text.length > 5000) {
        charCount.style.color = '#ffc107';
    } else {
        charCount.style.color = '#28a745';
    }
}

function validateInput() {
    const text = newsTextArea.value.trim();
    const isValid = text.length >= 10;
    
    analyzeBtn.disabled = !isValid || isAnalyzing;
    
    if (text.length > 0 && text.length < 10) {
        showStatus('Text must be at least 10 characters long', 'error');
    } else if (text.length >= 10) {
        showStatus('Ready to analyze', 'success');
    } else {
        showStatus('Ready to analyze', 'default');
    }
}

async function handleFormSubmit(event) {
    event.preventDefault();
    
    const text = newsTextArea.value.trim();
    
    if (text.length < 10) {
        showError('Please enter at least 10 characters of text.');
        return;
    }
    
    if (isAnalyzing) {
        return;
    }
    
    await analyzeText(text);
}

async function analyzeText(text) {
    setAnalyzingState(true);
    
    try {
        showStatus('Analyzing article...', 'loading');
        
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP ${response.status}`);
        }
        
        const result = await response.json();
        
        showStatus('Analysis complete!', 'success');
        displayResults(result);
        
    } catch (error) {
        console.error('Analysis error:', error);
        showStatus('Analysis failed', 'error');
        showError(`Failed to analyze text: ${error.message}`);
    } finally {
        setAnalyzingState(false);
    }
}

function setAnalyzingState(analyzing) {
    isAnalyzing = analyzing;
    
    if (analyzing) {
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
        loadingSpinner.style.display = 'inline-block';
    } else {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-search me-2"></i>Analyze Article';
        loadingSpinner.style.display = 'none';
    }
}

function showStatus(message, type = 'default') {
    statusText.textContent = message;
    
    // Reset classes
    statusIndicator.className = '';
    
    // Add appropriate class
    switch (type) {
        case 'loading':
            statusIndicator.classList.add('loading');
            loadingSpinner.style.display = 'inline-block';
            break;
        case 'success':
            statusIndicator.classList.add('success');
            loadingSpinner.style.display = 'none';
            break;
        case 'error':
            statusIndicator.classList.add('error');
            loadingSpinner.style.display = 'none';
            break;
        default:
            loadingSpinner.style.display = 'none';
    }
}

function displayResults(result) {
    const isFake = result.prediction === 'FAKE';
    const confidence = Math.round(result.confidence * 100);
    
    const resultHtml = `
        <div class="result-card ${isFake ? 'result-fake' : 'result-real'} p-4 rounded fade-in">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h4 class="mb-2">
                        <i class="fas ${isFake ? 'fa-exclamation-triangle' : 'fa-check-circle'} me-2"></i>
                        ${result.prediction}
                    </h4>
                    <p class="mb-0">
                        This article appears to be <strong>${result.prediction.toLowerCase()}</strong> news
                        with ${confidence}% confidence.
                    </p>
                </div>
                <div class="col-md-4 text-center">
                    <div class="confidence-display">
                        <div class="h2 mb-0">${confidence}%</div>
                        <small>Confidence</small>
                    </div>
                </div>
            </div>
            
            <div class="mt-3">
                <div class="confidence-bar bg-light">
                    <div class="confidence-fill bg-white" style="width: ${confidence}%"></div>
                </div>
            </div>
        </div>
        
        ${result.text_stats ? generateStatsHtml(result.text_stats) : ''}
        ${result.sentiment_analysis ? generateSentimentHtml(result.sentiment_analysis) : ''}
    `;
    
    resultsContent.innerHTML = resultHtml;
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function generateStatsHtml(stats) {
    return `
        <div class="mt-4">
            <h6 class="text-dark mb-3">
                <i class="fas fa-chart-bar me-2"></i>Text Statistics
            </h6>
            <div class="stats-grid">
                <div class="stat-item bg-light rounded">
                    <span class="stat-value text-primary">${stats.length || 0}</span>
                    <span class="stat-label">Characters</span>
                </div>
                <div class="stat-item bg-light rounded">
                    <span class="stat-value text-primary">${stats.word_count || 0}</span>
                    <span class="stat-label">Words</span>
                </div>
                <div class="stat-item bg-light rounded">
                    <span class="stat-value text-primary">${stats.sentence_count || 0}</span>
                    <span class="stat-label">Sentences</span>
                </div>
                <div class="stat-item bg-light rounded">
                    <span class="stat-value text-primary">${stats.avg_word_length || 0}</span>
                    <span class="stat-label">Avg Word Length</span>
                </div>
            </div>
        </div>
    `;
}

function generateSentimentHtml(sentiment) {
    const sentimentClass = `sentiment-${sentiment.sentiment}`;
    const sentimentIcon = sentiment.sentiment === 'positive' ? 'fa-smile' : 
                         sentiment.sentiment === 'negative' ? 'fa-frown' : 'fa-meh';
    
    return `
        <div class="mt-4">
            <h6 class="text-dark mb-3">
                <i class="fas fa-heart me-2"></i>Sentiment Analysis
            </h6>
            <div class="bg-light p-3 rounded">
                <div class="row">
                    <div class="col-md-4 text-center">
                        <i class="fas ${sentimentIcon} fa-2x ${sentimentClass}"></i>
                        <div class="mt-2">
                            <strong class="${sentimentClass}">${sentiment.sentiment.toUpperCase()}</strong>
                        </div>
                    </div>
                    <div class="col-md-4 text-center">
                        <div class="text-muted">Polarity</div>
                        <div class="h5">${sentiment.polarity}</div>
                    </div>
                    <div class="col-md-4 text-center">
                        <div class="text-muted">Subjectivity</div>
                        <div class="h5">${sentiment.subjectivity}</div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function showError(message) {
    const errorHtml = `
        <div class="error-message">
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
        </div>
    `;
    resultsContent.innerHTML = errorHtml;
    resultsSection.style.display = 'block';
}

function clearText() {
    newsTextArea.value = '';
    resultsSection.style.display = 'none';
    updateCharacterCount();
    showStatus('Ready to analyze', 'default');
    newsTextArea.focus();
}

function scrollToAnalyzer() {
    document.getElementById('analyzer').scrollIntoView({ behavior: 'smooth' });
    setTimeout(() => {
        newsTextArea.focus();
    }, 500);
}

async function checkApiHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        
        if (response.ok) {
            const data = await response.json();
            if (data.model_loaded) {
                showStatus('API connected and model loaded', 'success');
            } else {
                showStatus('API connected but model not loaded', 'error');
            }
        } else {
            throw new Error('API not responding');
        }
    } catch (error) {
        console.error('API health check failed:', error);
        showStatus('API connection failed - check if backend is running', 'error');
    }
}

// Sample text function for testing
function loadSampleText(type = 'fake') {
    const sampleTexts = {
        fake: `BREAKING: Scientists discover that drinking coffee can make you live forever! 
               This one weird trick that doctors don't want you to know has been hiding in plain sight. 
               Big pharma companies are trying to suppress this information because it would destroy their profits. 
               Click here to learn the secret that the government doesn't want you to know!`,
        
        real: `Scientists at Stanford University published a new study in the Journal of Medical Research 
               showing that moderate coffee consumption may be associated with reduced risk of certain diseases. 
               The peer-reviewed study followed 10,000 participants over 15 years and found statistically 
               significant correlations between coffee intake and health outcomes. However, researchers 
               caution that more studies are needed to establish causation.`
    };
    
    newsTextArea.value = sampleTexts[type];
    updateCharacterCount();
    validateInput();
}

// Add sample text buttons (can be called from console for testing)
window.loadSampleText = loadSampleText;
window.clearText = clearText;
window.scrollToAnalyzer = scrollToAnalyzer;
