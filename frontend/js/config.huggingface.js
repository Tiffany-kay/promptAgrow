// Configuration for PromptAgro Frontend
window.CONFIG = {
    // API Configuration
    API: {
        // Replace 'your-username' and 'your-space-name' with your actual HF details
        BASE_URL: 'https://your-username-your-space-name.hf.space',
        TIMEOUT: 60000, // 60 seconds for image generation
        
        // Endpoints
        ENDPOINTS: {
            HEALTH: '/',
            GENERATE: '/generate/',
            PACKAGING: '/generate-packaging/'
        }
    },
    
    // Image generation settings
    GENERATION: {
        DEFAULT_SIZE: 768,
        MAX_SIZE: 1024,
        MIN_SIZE: 512,
        DEFAULT_STEPS: 6,
        MAX_STEPS: 10
    },
    
    // UI Configuration
    UI: {
        SHOW_ADVANCED: true,
        ENABLE_PREVIEW: true,
        AUTO_DOWNLOAD: false
    }
};
