// Configuration file for PKL Frontend
window.CONFIG = {
    // Backend API Configuration
    API: {
        // Local backend URL for testing the fix
        BASE_URL: 'http://localhost:8001/api',
        
        // Production backend URL 
        // BASE_URL: 'https://promptagrow.onrender.com/api',
        
        // Request timeout in milliseconds
        TIMEOUT: 30000,
        
        // Maximum file upload size (10MB)
        MAX_FILE_SIZE: 10 * 1024 * 1024,
        
        // Supported image formats
        SUPPORTED_FORMATS: ['image/jpeg', 'image/png', 'image/webp']
    },
    
    // Application Settings
    APP: {
        // Default language
        DEFAULT_LANGUAGE: 'en',
        
        // Available languages
        LANGUAGES: ['en', 'sw', 'fr'],
        
        // Form validation
        MIN_PRODUCT_NAME_LENGTH: 2,
        MAX_STORY_LENGTH: 500,
        
        // Progress simulation timing
        PROGRESS_UPDATE_INTERVAL: 800,
        MAX_PROGRESS_TIME: 5000
    },
    
    // Feature flags
    FEATURES: {
        // Enable/disable user accounts
        USER_ACCOUNTS: true,
        
        // Enable/disable design regeneration
        DESIGN_REGENERATION: true,
        
        // Enable/disable social sharing
        SOCIAL_SHARING: true,
        
        // Enable debug mode
        DEBUG: false
    }
};
