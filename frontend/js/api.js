// API Communication Module
class API {
    constructor() {
        // Check if we should use Hugging Face Space
        this.useHuggingFace = window.CONFIG?.API?.BASE_URL?.includes('hf.space');
        
        if (this.useHuggingFace) {
            this.hfAPI = new HuggingFaceAPI();
            this.baseURL = this.hfAPI.baseURL;
        } else {
            // Use local backend
            this.baseURL = window.CONFIG?.API?.BASE_URL || 'http://localhost:8000/api';
        }
        
        this.timeout = window.CONFIG?.API?.TIMEOUT || 30000;
    }

    // Generate packaging design
    async generatePackaging(formData) {
        try {
            // If using Hugging Face, convert FormData to object
            if (this.useHuggingFace && this.hfAPI) {
                const productData = {};
                for (let [key, value] of formData.entries()) {
                    if (key === 'preferredColors') {
                        try {
                            productData[key] = JSON.parse(value);
                        } catch {
                            productData[key] = [value];
                        }
                    } else {
                        productData[key] = value;
                    }
                }
                
                console.log('🚀 Using Hugging Face Space API');
                return await this.hfAPI.generatePackaging(productData);
            }
            
            // Use local backend
            const response = await this.request('/generate', {
                method: 'POST',
                body: formData // FormData object with image and form fields
            });
            
            if (response.success) {
                return response.data;
            } else {
                throw new Error(response.error || 'Failed to generate packaging');
            }
        } catch (error) {
            console.error('Packaging generation failed:', error);
            return this.handleError(error);
        }
    }
    
    // Generate packaging design using Replicate API
    async generatePackagingWithReplicate(formData) {
        try {
            const response = await this.request('/generate-replicate', {
                method: 'POST',
                body: formData // FormData object with image and form fields
            });

            if (response.success) {
                return response.data; // Return the data directly
            } else {
                throw new Error(response.error || 'Failed to generate packaging with Replicate');
            }
        } catch (error) {
            console.error('Replicate packaging generation failed:', error);
            return this.handleError(error);
        }
    }

    // Generic API request method  
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            timeout: this.timeout,
            ...options
        };
        
        // Don't set Content-Type for FormData (let browser set it)
        if (!(options.body instanceof FormData)) {
            config.headers = {
                'Content-Type': 'application/json',
                ...options.headers
            };
        }
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
            }
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return await response.text();
        } catch (error) {
            console.error('API request failed:', error);
            return this.handleError(error);
        }
    }
    
    // Regenerate design with customizations
    async regenerateDesign(designId, customizations) {
        try {
            const response = await this.request('/regenerate', {
                method: 'POST',
                body: JSON.stringify({
                    designId,
                    customizations,
                    language: window.i18n.currentLanguage
                })
            });
            
            if (response.success) {
                return response.data;
            } else {
                throw new Error(response.error || 'Failed to regenerate design');
            }
        } catch (error) {
            console.error('Design regeneration failed:', error);
            return this.handleError(error);
        }
    }
    
    // Save design to user account
    async saveDesign(designId, userEmail, designName) {
        try {
            const response = await this.request('/save-design', {
                method: 'POST',
                body: JSON.stringify({
                    designId,
                    userEmail,
                    designName
                })
            });
            
            if (response.success) {
                return response;
            } else {
                throw new Error(response.error || 'Failed to save design');
            }
        } catch (error) {
            console.error('Design save failed:', error);
            return this.handleError(error);
        }
    }
    
    // Get user's saved designs
    async getUserDesigns() {
        // Mock API call
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    success: true,
                    designs: []
                });
            }, 1000);
        });
    }
    
    // Upload image file
    async uploadImage(file) {
        // Mock file processing
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                resolve({
                    success: true,
                    imageUrl: e.target.result,
                    fileName: file.name
                });
            };
            reader.readAsDataURL(file);
        });
    }
    
    // Handle errors gracefully
    handleError(error) {
        const errorMessages = {
            'Failed to fetch': 'Network error. Please check your connection.',
            'HTTP 400': 'Invalid request. Please check your inputs.',
            'HTTP 401': 'Authentication required. Please log in.',
            'HTTP 403': 'Access denied.',
            'HTTP 404': 'Service not found.',
            'HTTP 500': 'Server error. Please try again later.'
        };
        
        const message = errorMessages[error.message] || 'An unexpected error occurred.';
        Components.showToast(message, 'error');
        
        return { success: false, error: message };
    }
}

// Create global API instance
window.api = new API();
