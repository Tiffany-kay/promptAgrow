// Application State Management
class AppState {
    constructor() {
        this.currentStep = 0;
        this.currentScreen = 'landing';
        this.currentLanguage = 'en';
        
        this.form = {
            image: null,
            imagePreview: null,
            productName: '',
            tagline: '',
            preferredColors: [],
            salesPlatform: 'local-market',
            desiredEmotion: 'trust',
            productStory: ''
        };
        
        this.preview = {
            mockupUrl: null,
            pdfUrl: null,
            customizations: {
                brightness: 100,
                contrast: 100,
                saturation: 100,
                fontStyle: 'serif',
                layout: 'top-label'
            }
        };
        
        this.loading = {
            isLoading: false,
            progress: 0,
            message: ''
        };
        
        this.observers = [];
    }
    
    // Subscribe to state changes
    subscribe(callback) {
        this.observers.push(callback);
    }
    
    // Notify observers of state changes
    notify(changedProperty, value) {
        this.observers.forEach(callback => callback(changedProperty, value));
    }
    
    // Update form data
    updateForm(field, value) {
        this.form[field] = value;
        this.notify('form', { field, value });
    }
    
    // Update preview data
    updatePreview(field, value) {
        this.preview[field] = value;
        this.notify('preview', { field, value });
    }
    
    // Update loading state
    updateLoading(field, value) {
        this.loading[field] = value;
        this.notify('loading', { field, value });
    }
    
    // Change current step
    setStep(step) {
        this.currentStep = step;
        this.notify('step', step);
    }
    
    // Change current screen
    setScreen(screen) {
        this.currentScreen = screen;
        this.notify('screen', screen);
    }
    
    // Change language
    setLanguage(language) {
        this.currentLanguage = language;
        this.notify('language', language);
    }
    
    // Get current state snapshot
    getState() {
        return {
            currentStep: this.currentStep,
            currentScreen: this.currentScreen,
            currentLanguage: this.currentLanguage,
            form: { ...this.form },
            preview: { ...this.preview },
            loading: { ...this.loading }
        };
    }
}

// Create global state instance
window.appState = new AppState();
