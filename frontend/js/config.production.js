// Production Configuration for PromptAgro Frontend
window.CONFIG = {
    // Backend API Configuration
    API: {
        // Production backend URL - UPDATE THIS WITH YOUR ACTUAL BACKEND URL
        BASE_URL: 'https://your-backend-domain.herokuapp.com/api',
        
        // Development fallback
        // BASE_URL: 'http://localhost:8000/api',
        
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
        
        // UI Settings
        PROGRESS_UPDATE_INTERVAL: 800,
        MAX_PROGRESS_TIME: 5000
    },
    
    // Feature Flags
    FEATURES: {
        // User account system
        USER_ACCOUNTS: true,
        
        // Design regeneration
        DESIGN_REGENERATION: true,
        
        // Social sharing
        SOCIAL_SHARING: true,
        
        // Debug mode (set to false in production)
        DEBUG: false
    },
    
    // Analytics (Optional)
    ANALYTICS: {
        GOOGLE_ANALYTICS_ID: 'G-XXXXXXXXXX',
        FACEBOOK_PIXEL_ID: 'XXXXXXXXXX'
    }
};
