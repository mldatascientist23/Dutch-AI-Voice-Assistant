// Configuration for different environments
window.APP_CONFIG = {
    // Determine API base URL dynamically
    getApiBaseUrl: function() {
        // If running in Docker/production with nginx proxy
        // API calls should go through /api/ proxy
        const hostname = window.location.hostname;
        const port = window.location.port;
        const protocol = window.location.protocol;
        
        // Check if we're accessing via nginx (production setup)
        // In production, API is available at /api/
        if (port === '80' || port === '443' || port === '') {
            // Production: use /api prefix for nginx proxy
            return `${protocol}//${hostname}/api`;
        } else if (hostname === 'localhost' || hostname === '127.0.0.1') {
            // Local development: direct backend connection
            return 'http://localhost:8000';
        } else {
            // Other cases: try /api prefix
            return `${protocol}//${hostname}/api`;
        }
    },
    
    // Get the computed API base URL
    API_BASE: null
};

// Initialize API_BASE on load
window.APP_CONFIG.API_BASE = window.APP_CONFIG.getApiBaseUrl();

console.log('API Base URL:', window.APP_CONFIG.API_BASE);
