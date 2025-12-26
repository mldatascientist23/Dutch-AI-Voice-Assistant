// Configuration for different environments
window.APP_CONFIG = {
    // localStorage key for backend URL
    STORAGE_KEY: 'dutch_ai_backend_url',
    
    // Determine API base URL dynamically
    getApiBaseUrl: function() {
        // First, check localStorage for user-configured backend URL
        const storedUrl = localStorage.getItem(this.STORAGE_KEY);
        if (storedUrl) {
            return storedUrl;
        }
        
        // Check for custom backend URL from environment variable or window config
        // This can be set via Vercel environment variables as BACKEND_API_URL
        if (window.BACKEND_API_URL) {
            return window.BACKEND_API_URL;
        }
        
        const hostname = window.location.hostname;
        const port = window.location.port;
        const protocol = window.location.protocol;
        
        // For local development (localhost with non-default port)
        // Check if we should use direct backend connection
        if ((hostname === 'localhost' || hostname === '127.0.0.1') && port && port !== '80' && port !== '443') {
            // When running frontend on localhost with a custom port,
            // try direct backend connection first
            return `${protocol}//${hostname}:8000`;
        }
        
        // For production or when on default ports (80/443)
        // Use nginx proxy with /api prefix
        const portSuffix = (port && port !== '80' && port !== '443') ? ':' + port : '';
        return `${protocol}//${hostname}${portSuffix}/api`;
    },
    
    // Save backend URL to localStorage
    setBackendUrl: function(url) {
        if (url) {
            // Remove any trailing slashes
            url = url.replace(/\/+$/, '');
            localStorage.setItem(this.STORAGE_KEY, url);
        } else {
            localStorage.removeItem(this.STORAGE_KEY);
        }
        // Reload to apply the new URL
        window.location.reload();
    },
    
    // Clear stored backend URL
    clearBackendUrl: function() {
        localStorage.removeItem(this.STORAGE_KEY);
        window.location.reload();
    },
    
    // Check if backend URL is user-configured (via localStorage)
    isUserConfigured: function() {
        return !!localStorage.getItem(this.STORAGE_KEY);
    },
    
    // Get the computed API base URL
    API_BASE: null
};

// Initialize API_BASE on load
window.APP_CONFIG.API_BASE = window.APP_CONFIG.getApiBaseUrl();

console.log('API Base URL:', window.APP_CONFIG.API_BASE);