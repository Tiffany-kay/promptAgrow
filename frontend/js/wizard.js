// Wizard Step Management
class Wizard {
    constructor() {
        this.steps = ['upload', 'story', 'preferences', 'magic', 'preview', 'download'];
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
        
        // Step 3: Preferences
        this.stepElements.set('preferences', this.createPreferencesStep());
        
        // Step 4: Magic (Loading)
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
                    <span data-i18n="common.next">Next</span>
                    <i class="fas fa-arrow-right"></i>
                </button>
            </div>
        `;
        return div;
    }
    
    // Create Preferences Step (Step 3)
    createPreferencesStep() {
        const div = document.createElement('div');
        div.className = 'step-content';
        div.innerHTML = `
            <div class="step-header">
                <h2>🎨 Design Preferences</h2>
                <p>Help us understand your brand vision</p>
            </div>
            <div class="form-container">
                <div class="form-group">
                    <label for="preferredColors">Preferred Colors</label>
                    <div class="color-selector">
                        <div class="color-options">
                            <label><input type="checkbox" name="preferredColors" value="red"> <span class="color-sample" style="background-color: #f44336"></span> Red</label>
                            <label><input type="checkbox" name="preferredColors" value="blue"> <span class="color-sample" style="background-color: #2196f3"></span> Blue</label>
                            <label><input type="checkbox" name="preferredColors" value="green"> <span class="color-sample" style="background-color: #4caf50"></span> Green</label>
                            <label><input type="checkbox" name="preferredColors" value="orange"> <span class="color-sample" style="background-color: #ff9800"></span> Orange</label>
                            <label><input type="checkbox" name="preferredColors" value="purple"> <span class="color-sample" style="background-color: #9c27b0"></span> Purple</label>
                            <label><input type="checkbox" name="preferredColors" value="yellow"> <span class="color-sample" style="background-color: #ffeb3b"></span> Yellow</label>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="salesPlatform">Where will you sell this?</label>
                    <select id="salesPlatform">
                        <option value="local-market">Local Market</option>
                        <option value="retail-store">Retail Store</option>
                        <option value="online-store">Online Store</option>
                        <option value="farmers-market">Farmer's Market</option>
                        <option value="wholesale">Wholesale</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="desiredEmotion">What feeling should your brand evoke?</label>
                    <select id="desiredEmotion">
                        <option value="trust">Trust & Reliability</option>
                        <option value="premium">Premium & Luxury</option>
                        <option value="natural">Natural & Organic</option>
                        <option value="fun">Fun & Playful</option>
                        <option value="traditional">Traditional & Heritage</option>
                        <option value="modern">Modern & Innovative</option>
                    </select>
                </div>
            </div>
            <div class="step-actions">
                <button class="btn-secondary" id="step3Back">
                    <i class="fas fa-arrow-left"></i>
                    <span data-i18n="common.back">Back</span>
                </button>
                <button class="btn-primary" id="step3Next">
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
            // Validate form before proceeding to preferences
            if (this.validateStoryForm()) {
                this.showStep(2); // Go to preferences step
            }
        } else if (event.target.id === 'step2Back') {
            this.showStep(0);
        } else if (event.target.id === 'step3Next') {
            // Validate preferences form before proceeding
            if (this.validatePreferencesForm()) {
                this.showStep(3); // Go to loading step
                // Call backend API
                window.app.submitToBackend();
            }
        } else if (event.target.id === 'step3Back') {
            this.showStep(1);
        } else if (event.target.id === 'step4Back') {
            this.showStep(2); // Back to preferences from preview
        } else if (event.target.id === 'step4Next') {
            this.showStep(5); // Go to download
        }
    }
    
    // Validate story form
    validateStoryForm() {
        const productName = document.getElementById('productName')?.value;
        if (!productName || productName.trim().length < 2) {
            Components.showToast('Please enter a product name', 'error');
            return false;
        }
        
        // Save form data to state
        const tagline = document.getElementById('tagline')?.value || '';
        const productStory = document.getElementById('productStory')?.value || '';
        
        appState.updateForm('productName', productName.trim());
        appState.updateForm('tagline', tagline.trim());
        appState.updateForm('productStory', productStory.trim());
        
        console.log('📝 Story form data saved:', { productName, tagline, productStory });
        
        const state = appState.getState();
        if (!state.form.image) {
            Components.showToast('Please upload a product image first', 'error');
            this.showStep(0); // Go back to upload
            return false;
        }
        
        return true;
    }
    
    // Validate preferences form
    validatePreferencesForm() {
        // All preferences are optional, but we should collect them
        // and store them in appState
        const selectedColors = [];
        const colorCheckboxes = document.querySelectorAll('input[name="preferredColors"]:checked');
        colorCheckboxes.forEach(cb => selectedColors.push(cb.value));
        
        const salesPlatform = document.getElementById('salesPlatform')?.value || 'local-market';
        const desiredEmotion = document.getElementById('desiredEmotion')?.value || 'trust';
        
        // Store preferences in app state
        appState.updateForm('preferredColors', selectedColors);
        appState.updateForm('salesPlatform', salesPlatform);
        appState.updateForm('desiredEmotion', desiredEmotion);
        
        console.log('🎨 Preferences collected:', { selectedColors, salesPlatform, desiredEmotion });
        
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
                    <h3>📦 Your Custom Packaging Design</h3>
                    ${previewData.mockupUrl ? 
                        `<img src="${previewData.mockupUrl}" alt="Packaging Design" class="mockup-image" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAwIiBoZWlnaHQ9IjYwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4gIDxyZWN0IHdpZHRoPSI4MDAiIGhlaWdodD0iNjAwIiBmaWxsPSIjMkU3RDMyIi8+ICA8dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1zaXplPSIyNCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7wn5OmIFlvdXIgUGFja2FnaW5nIERlc2lnbjwvdGV4dD48L3N2Zz4='" />` :
                        `<div class="mockup-placeholder">
                            <i class="fas fa-image"></i>
                            <p>Generating your packaging image...</p>
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
