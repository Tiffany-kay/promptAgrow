// Main Application Controller
class App {
    constructor() {
        this.wizard = new Wizard();
        this.currentScreen = 'landing';
    }

    // Initialize the application
    async init() {
        try {
            // Load default language
            await i18n.loadTranslations('en');
            await i18n.setLanguage('en');
            
            // Setup event listeners
            this.bindEvents();
            
            // Show landing screen
            this.showScreen('landing');
            
            console.log('PromptAgro app initialized successfully');
        } catch (error) {
            console.error('Failed to initialize app:', error);
            Components.showToast('Failed to load application', 'error');
        }
    }
    
    // Bind global event listeners
    bindEvents() {
        // Start button on landing page
        const startButton = document.getElementById('startButton');
        if (startButton) {
            startButton.addEventListener('click', () => this.startWizard());
        }
        
        // Language selector
        const languageSelect = document.getElementById('languageSelect');
        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                i18n.setLanguage(e.target.value);
                appState.setLanguage(e.target.value);
            });
        }
        
        // File upload handling
        this.bindFileUpload();
        
        // Form field changes
        this.bindFormFields();
        
        // Listen to state changes
        appState.subscribe(this.handleStateChange.bind(this));
    }
    
    // Handle file upload events
    bindFileUpload() {
        // Use event delegation since elements may not exist yet
        document.addEventListener('change', (e) => {
            if (e.target.id === 'imageInput') {
                this.handleImageUpload(e);
            }
        });
        
        document.addEventListener('click', (e) => {
            if (e.target.id === 'browseButton') {
                const imageInput = document.getElementById('imageInput');
                if (imageInput) imageInput.click();
            } else if (e.target.id === 'changeImage') {
                const imageInput = document.getElementById('imageInput');
                if (imageInput) imageInput.click();
            }
        });
        
        // Use event delegation for drag and drop
        document.addEventListener('dragover', (e) => {
            if (e.target.closest('#uploadZone')) {
                this.handleDragOver(e);
            }
        });
        
        document.addEventListener('drop', (e) => {
            if (e.target.closest('#uploadZone')) {
                this.handleDrop(e);
            }
        });
    }
    
    // Handle form field changes
    bindFormFields() {
        const fields = ['productName', 'tagline', 'productStory'];
        
        fields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', (e) => {
                    appState.updateForm(fieldId, e.target.value);
                });
            }
        });
    }
    
    // Show specific screen
    showScreen(screenName) {
        const screens = document.querySelectorAll('.screen');
        screens.forEach(screen => screen.classList.remove('active'));
        
        const targetScreen = document.getElementById(screenName);
        if (targetScreen) {
            targetScreen.classList.add('active');
        }
        
        this.currentScreen = screenName;
        appState.setScreen(screenName);
    }
    
    // Start the wizard
    startWizard() {
        // Hide landing screen
        const landingScreen = document.getElementById('landing');
        if (landingScreen) {
            landingScreen.classList.remove('active');
        }
        
        // Show wizard container
        const wizardContainer = document.getElementById('wizard');
        if (wizardContainer) {
            wizardContainer.classList.add('active');
            wizardContainer.style.display = 'block';
            
            // Add progress bar
            const progressBar = document.getElementById('progressBar');
            if (progressBar) {
                progressBar.innerHTML = Components.createProgressBar();
            }
            
            // Initialize wizard steps
            this.wizard.init();
        }
    }
    
    // Handle image upload
    async handleImageUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        if (!file.type.startsWith('image/')) {
            Components.showToast('Please select a valid image file', 'error');
            return;
        }
        
        try {
            const result = await api.uploadImage(file);
            if (result.success) {
                appState.updateForm('image', file);
                appState.updateForm('imagePreview', result.imageUrl);
                this.showImagePreview(result.imageUrl);
                Components.showToast('Image uploaded successfully!', 'success');
            }
        } catch (error) {
            Components.showToast('Failed to upload image', 'error');
        }
    }
    
    // Show image preview
    showImagePreview(imageUrl) {
        const uploadZone = document.getElementById('uploadZone');
        const imagePreview = document.getElementById('imagePreview');
        const previewImage = document.getElementById('previewImage');
        const nextButton = document.getElementById('step1Next');
        
        if (uploadZone) uploadZone.style.display = 'none';
        if (imagePreview) imagePreview.style.display = 'block';
        if (previewImage) previewImage.src = imageUrl;
        if (nextButton) nextButton.disabled = false;
    }
    
    // Handle drag over
    handleDragOver(event) {
        event.preventDefault();
        event.currentTarget.classList.add('drag-over');
    }
    
    // Handle file drop
    handleDrop(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('drag-over');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            const imageInput = document.getElementById('imageInput');
            if (imageInput) {
                imageInput.files = files;
                this.handleImageUpload({ target: { files } });
            }
        }
    }
    
    // Create FormData for backend API
    createFormDataForAPI() {
        const formData = new FormData();
        const state = appState.getState();
        
        console.log('🔍 Current app state:', state);
        
        // Add image file
        if (state.form.image) {
            formData.append('image', state.form.image);
            console.log('📷 Image added:', state.form.image.name, state.form.image.size, 'bytes');
        } else {
            console.error('❌ No image found in state!');
        }
        
        // Add form fields
        formData.append('productName', state.form.productName || '');
        formData.append('tagline', state.form.tagline || '');
        formData.append('preferredColors', JSON.stringify(state.form.preferredColors || []));
        formData.append('salesPlatform', state.form.salesPlatform || 'local-market');
        formData.append('desiredEmotion', state.form.desiredEmotion || 'trust');
        formData.append('productStory', state.form.productStory || '');
        formData.append('language', state.currentLanguage || 'en');
        
        // Debug log all form data
        console.log('📦 FormData contents:');
        for (let [key, value] of formData.entries()) {
            if (key === 'image') {
                console.log(`  ${key}:`, value.name, value.size, 'bytes', value.type);
            } else {
                console.log(`  ${key}:`, value);
            }
        }
        
        return formData;
    }
    
    // Submit form to backend
    async submitToBackend() {
        try {
            // Update loading state
            appState.updateLoading('isLoading', true);
            appState.updateLoading('progress', 0);
            appState.updateLoading('message', 'Preparing your design...');
            
            // Create form data
            const formData = this.createFormDataForAPI();
            
            // Simulate progress updates
            this.simulateProgress();
            
            // Call backend API
            const result = await api.generatePackaging(formData);
            
            console.log('🎯 Backend API Result:', result);
            
            if (result && !result.error) {
                console.log('✅ Processing successful result:', result);
                
                // Convert relative URLs to absolute URLs
                const baseURL = 'https://promptagrow.onrender.com';
                const mockupUrl = result.mockupUrl.startsWith('http') ? result.mockupUrl : `${baseURL}${result.mockupUrl}`;
                const reportUrl = result.reportUrl.startsWith('http') ? result.reportUrl : `${baseURL}${result.reportUrl}`;
                
                console.log('🔗 Converted URLs:', { mockupUrl, reportUrl });
                
                // Store results in state with absolute URLs
                appState.updatePreview('mockupUrl', mockupUrl);
                appState.updatePreview('pdfUrl', reportUrl);
                appState.updatePreview('designId', result.designId);
                appState.updatePreview('concepts', result.concepts);
                appState.updatePreview('colorPalette', result.colorPalette);
                appState.updatePreview('stylesSuggestions', result.stylesSuggestions);
                appState.updatePreview('aiConfidence', result.aiConfidence);
                
                // Create result object with absolute URLs for display
                const displayResult = {
                    ...result,
                    mockupUrl: mockupUrl,
                    reportUrl: reportUrl
                };
                
                // Move to preview step
                this.wizard.showStep(3); // Preview step
                
                // Display the preview data
                setTimeout(() => {
                    console.log('🎨 Calling displayPreview with:', displayResult);
                    if (this.wizard && this.wizard.displayPreview) {
                        this.wizard.displayPreview(displayResult);
                    } else {
                        console.error('❌ displayPreview method not found on wizard');
                    }
                }, 500);
                
                Components.showToast('Design generated successfully!', 'success');
            } else {
                throw new Error(result.error || 'Failed to generate design');
            }
        } catch (error) {
            console.error('Backend submission failed:', error);
            Components.showToast('Failed to generate design. Please try again.', 'error');
        } finally {
            appState.updateLoading('isLoading', false);
        }
    }
    
    // Simulate progress for better UX
    simulateProgress() {
        let progress = 0;
        const messages = [
            'Analyzing your product...',
            'Generating design concepts...',
            'Creating mockup...',
            'Finalizing design...'
        ];
        
        const interval = setInterval(() => {
            progress += Math.random() * 20;
            if (progress > 90) progress = 90;
            
            appState.updateLoading('progress', progress);
            
            const messageIndex = Math.floor(progress / 25);
            if (messages[messageIndex]) {
                appState.updateLoading('message', messages[messageIndex]);
            }
        }, 800);
        
        // Clear interval when done
        setTimeout(() => clearInterval(interval), 5000);
    }

    // Handle state changes
    handleStateChange(property, value) {
        if (property === 'language') {
            i18n.updatePageTranslations();
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
    app.init();
});
