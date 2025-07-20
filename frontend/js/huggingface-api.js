// HuggingFace Space API Integration
class HuggingFaceAPI {
    constructor() {
        this.baseURL = window.CONFIG?.API?.BASE_URL || 'https://your-username-your-space-name.hf.space';
        this.timeout = window.CONFIG?.API?.TIMEOUT || 60000;
    }
    
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL}/`, {
                method: 'GET',
                timeout: 10000
            });
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            return { status: 'error', error: error.message };
        }
    }
    
    async generatePackaging(productData) {
        try {
            console.log('🚀 Sending to HuggingFace Space:', productData);
            
            // Create form data for the API
            const formData = new FormData();
            formData.append('product_name', productData.productName || 'Agricultural Product');
            formData.append('colors', (productData.preferredColors || ['green']).join(','));
            formData.append('emotion', productData.desiredEmotion || 'trust');
            formData.append('platform', productData.salesPlatform || 'farmers-market');
            
            const response = await fetch(`${this.baseURL}/generate-packaging/`, {
                method: 'POST',
                body: formData,
                timeout: this.timeout
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const result = await response.json();
            
            if (result.success) {
                return {
                    success: true,
                    data: {
                        mockupUrl: result.image_data, // Base64 image
                        designId: `hf_${Date.now()}`,
                        generator: result.generator,
                        cost: result.cost,
                        processingTime: result.processing_time,
                        promptUsed: result.prompt_used,
                        // Add some mock data for compatibility
                        concepts: [
                            `Premium ${productData.productName} - AI Generated`,
                            `Professional packaging design`,
                            `${productData.desiredEmotion} focused branding`
                        ],
                        stylesSuggestions: ['Modern', 'Professional', 'Agricultural'],
                        colorPalette: productData.preferredColors || ['#2E7D32', '#4CAF50'],
                        aiConfidence: 0.92
                    }
                };
            } else {
                throw new Error(result.error || 'Generation failed');
            }
            
        } catch (error) {
            console.error('HuggingFace API error:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    async generateBasic(prompt, options = {}) {
        try {
            const formData = new FormData();
            formData.append('prompt', prompt);
            formData.append('width', options.width || 768);
            formData.append('height', options.height || 768);
            formData.append('num_inference_steps', options.steps || 6);
            formData.append('guidance_scale', options.guidance || 1.5);
            
            const response = await fetch(`${this.baseURL}/generate/`, {
                method: 'POST',
                body: formData,
                timeout: this.timeout
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
            
        } catch (error) {
            console.error('Basic generation failed:', error);
            return { success: false, error: error.message };
        }
    }
}

// Make it globally available
window.HuggingFaceAPI = HuggingFaceAPI;
