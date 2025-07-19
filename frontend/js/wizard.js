// Wizard Step Management
class Wizard {
    constructor() {
        this.steps = ['upload', 'story', 'magic', 'preview', 'download'];
        this.currentStep = 0;
        this.stepElements = new Map();
    }
    
    // Initialize wizard
    init() {
        const container = document.getElementById('stepContainer');
        if (!container) {
            return;
        }
        
        this.createStepElements();
        this.bindEvents();
        this.showStep(0);
    }
    
    // Create step HTML elements
    createStepElements() {
        const container = document.getElementById('stepContainer');
        
        // Step 1: Upload
        this.stepElements.set('upload', this.createUploadStep());
        
        // Step 2: Story
        this.stepElements.set('story', this.createStoryStep());
        
        // Step 3: Magic (Loading)
        this.stepElements.set('magic', this.createMagicStep());
        
        // Step 4: Preview
        this.stepElements.set('preview', this.createPreviewStep());
        
        // Step 5: Download
        this.stepElements.set('download', this.createDownloadStep());
        
        // Add all steps to container
        this.stepElements.forEach((element, step) => {
            element.style.display = 'none';
            container.appendChild(element);
        });
    }
    
    // Create upload step
    createUploadStep() {
        const div = document.createElement('div');
        div.className = 'step-content';
        div.innerHTML = `
            <div class="step-header">
                <h2 data-i18n="step1.title">📸 Upload Your Product Photo</h2>
                <p data-i18n="step1.subtitle">Show us what makes your harvest special</p>
            </div>
            
            <div class="upload-container">
                <div class="upload-zone" id="uploadZone">
                    <div class="upload-content">
                        <i class="fas fa-cloud-upload-alt upload-icon"></i>
                        <h3 data-i18n="step1.dragDrop">Drag & Drop Your Photo Here</h3>
                        <p data-i18n="step1.or">or</p>
                        <button class="upload-button" id="browseButton">
                            <i class="fas fa-folder-open"></i>
                            <span data-i18n="step1.browse">Browse Files</span>
                        </button>
                        <input type="file" id="imageInput" accept="image/*" hidden>
                        <div class="upload-tip">
                            <i class="fas fa-lightbulb"></i>
                            <span data-i18n="step1.tip">Pro tip: Bright, clear shots = better mockups</span>
                        </div>
                    </div>
                </div>
                
                <div class="image-preview" id="imagePreview" style="display: none;">
                    <img id="previewImage" alt="Preview">
                    <div class="image-actions">
                        <button class="btn-secondary" id="changeImage">
                            <i class="fas fa-exchange-alt"></i>
                            <span data-i18n="step1.change">Change Photo</span>
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="step-actions">
                <div></div>
                <button class="btn-primary" id="step1Next" disabled>
                    <span data-i18n="common.next">Next Step</span>
                    <i class="fas fa-arrow-right"></i>
                </button>
            </div>
        `;
        return div;
    }
    
    // Create story step
    createStoryStep() {
        const div = document.createElement('div');
        div.className = 'step-content';
        div.innerHTML = `
            <div class="step-header">
                <h2 data-i18n="step2.title">✍️ Tell Your Product's Story</h2>
                <p data-i18n="step2.subtitle">Every great harvest has a story worth sharing</p>
            </div>
            <div class="form-container">
                <div class="form-group">
                    <label for="productName" data-i18n="step2.productName">Product Name</label>
                    <input type="text" id="productName" placeholder="e.g., Achieng's Golden Honey">
                </div>
                <div class="form-group">
                    <label for="tagline" data-i18n="step2.tagline">Catchy Tagline</label>
                    <input type="text" id="tagline" placeholder="e.g., Pure sweetness from the hills">
                </div>
                <div class="form-group">
                    <label for="productStory" data-i18n="step2.story">Your Product's Story</label>
                    <textarea id="productStory" rows="4" placeholder="Tell us about your journey..."></textarea>
                </div>
            </div>
            <div class="step-actions">
                <button class="btn-secondary" id="step2Back">
                    <i class="fas fa-arrow-left"></i>
                    <span data-i18n="common.back">Back</span>
                </button>
                <button class="btn-primary" id="step2Next">
                    <span data-i18n="common.next">Create Magic</span>
                    <i class="fas fa-magic"></i>
                </button>
            </div>
        `;
        return div;
    }
    
    // Create remaining steps (simplified for brevity)
    createMagicStep() {
        const div = document.createElement('div');
        div.className = 'step-content';
        div.innerHTML = Components.createLoadingSpinner('Creating your magical packaging...');
        return div;
    }
    
    createPreviewStep() {
        const div = document.createElement('div');
        div.className = 'step-content';
        div.innerHTML = `
            <div class="preview-container">
                <div class="step-header">
                    <h2>🎨 Your Design Preview</h2>
                    <p>Here's your AI-generated packaging design</p>
                </div>
                
                <div id="previewContent" class="preview-content">
                    <div class="preview-loading">
                        <i class="fas fa-spinner fa-spin"></i>
                        <p>Loading your design...</p>
                    </div>
                </div>
                
                <div class="preview-actions" style="display: none;">
                    <button type="button" class="btn-secondary" onclick="window.wizard.showStep(1)">
                        <i class="fas fa-arrow-left"></i> Back to Edit
                    </button>
                    <button type="button" class="btn-primary" id="regenerateBtn">
                        <i class="fas fa-sync"></i> Regenerate Design
                    </button>
                    <button type="button" class="btn-accent" onclick="window.wizard.showStep(4)">
                        <i class="fas fa-download"></i> Download
                    </button>
                </div>
            </div>
        `;
        return div;
    }
    
    createDownloadStep() {
        const div = document.createElement('div');
        div.className = 'step-content';
        div.innerHTML = '<div class="download-container">Download options will appear here</div>';
        return div;
    }
    
    // Show specific step
    showStep(stepIndex) {
        this.currentStep = stepIndex;
        const stepName = this.steps[stepIndex];
        
        // Hide all steps
        this.stepElements.forEach((element) => {
            element.style.display = 'none';
        });
        
        // Show current step
        if (this.stepElements.has(stepName)) {
            this.stepElements.get(stepName).style.display = 'block';
        }
        
        // Update progress
        this.updateProgress();
        appState.setStep(stepIndex);
    }
    
    // Update progress bar
    updateProgress() {
        const progress = ((this.currentStep + 1) / this.steps.length) * 100;
        const progressFill = document.getElementById('progressFill');
        if (progressFill) {
            progressFill.style.width = `${progress}%`;
        }
        
        // Update step indicators
        const stepElements = document.querySelectorAll('.step');
        stepElements.forEach((element, index) => {
            element.classList.toggle('active', index <= this.currentStep);
        });
    }
    
    // Bind event handlers
    bindEvents() {
        // Navigation events will be bound here
        document.addEventListener('click', this.handleNavigation.bind(this));
    }
    
    // Handle navigation clicks
    handleNavigation(event) {
        if (event.target.id === 'step1Next') {
            this.showStep(1);
        } else if (event.target.id === 'step2Next') {
            // Validate form before proceeding
            if (this.validateStoryForm()) {
                this.showStep(2); // Go to loading step
                // Call backend API
                window.app.submitToBackend();
            }
        } else if (event.target.id === 'step2Back') {
            this.showStep(0);
        } else if (event.target.id === 'step4Back') {
            this.showStep(1); // Back to story from preview
        } else if (event.target.id === 'step4Next') {
            this.showStep(4); // Go to download
        }
    }
    
    // Validate story form
    validateStoryForm() {
        const productName = document.getElementById('productName')?.value;
        if (!productName || productName.trim().length < 2) {
            Components.showToast('Please enter a product name', 'error');
            return false;
        }
        
        const state = appState.getState();
        if (!state.form.image) {
            Components.showToast('Please upload a product image first', 'error');
            this.showStep(0); // Go back to upload
            return false;
        }
        
        return true;
    }
    
    // Display the generated design preview
    displayPreview(previewData) {
        console.log('🎨 displayPreview called with:', previewData);
        
        const previewContent = document.getElementById('previewContent');
        const previewActions = document.querySelector('.preview-actions');
        
        console.log('📄 previewContent element:', previewContent);
        console.log('🔘 previewActions element:', previewActions);
        
        if (!previewContent) {
            console.error('❌ previewContent element not found!');
            return;
        }
        
        // Build preview HTML
        let previewHTML = `
            <div class="design-preview">
                <div class="design-mockup">
                    <h3>📦 Packaging Design</h3>
                    ${previewData.mockupUrl ? 
                        `<img src="${previewData.mockupUrl}" alt="Packaging Design" class="mockup-image" />` :
                        `<div class="mockup-placeholder">
                            <i class="fas fa-box"></i>
                            <p>Design mockup will appear here</p>
                        </div>`
                    }
                </div>
                
                <div class="design-details">
                    <h3>🎯 Design Concepts</h3>
                    <div class="concepts-list">
                        ${previewData.concepts && previewData.concepts.length > 0 ? 
                            previewData.concepts.map(concept => `<div class="concept-item">• ${concept}</div>`).join('') :
                            '<div class="concept-item">• Premium agricultural branding</div><div class="concept-item">• Fresh and natural appeal</div><div class="concept-item">• Trust and quality focus</div>'
                        }
                    </div>
                    
                    ${previewData.colorPalette && previewData.colorPalette.length > 0 ? `
                        <h4>🎨 Color Palette</h4>
                        <div class="color-palette">
                            ${previewData.colorPalette.map(color => `<div class="color-swatch" style="background-color: ${color}" title="${color}"></div>`).join('')}
                        </div>
                    ` : ''}
                    
                    ${previewData.stylesSuggestions && previewData.stylesSuggestions.length > 0 ? `
                        <h4>✨ Style Suggestions</h4>
                        <div class="styles-list">
                            ${previewData.stylesSuggestions.map(style => `<div class="style-item">• ${style}</div>`).join('')}
                        </div>
                    ` : ''}
                    
                    ${previewData.designId ? `
                        <div class="design-info">
                            <small>Design ID: ${previewData.designId}</small>
                            ${previewData.aiConfidence ? `<small>AI Confidence: ${(previewData.aiConfidence * 100).toFixed(1)}%</small>` : ''}
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
        
        previewContent.innerHTML = previewHTML;
        
        // Show actions
        if (previewActions) {
            previewActions.style.display = 'flex';
        }
    }
}

window.Wizard = Wizard;
