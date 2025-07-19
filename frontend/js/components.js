// Reusable UI Components
class Components {
    // Create progress bar component
    static createProgressBar() {
        return `
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="progress-steps">
                    <div class="step active" data-step="1">
                        <i class="fas fa-camera"></i>
                        <span data-i18n="steps.upload">Upload</span>
                    </div>
                    <div class="step" data-step="2">
                        <i class="fas fa-edit"></i>
                        <span data-i18n="steps.story">Story</span>
                    </div>
                    <div class="step" data-step="3">
                        <i class="fas fa-magic"></i>
                        <span data-i18n="steps.magic">Magic</span>
                    </div>
                    <div class="step" data-step="4">
                        <i class="fas fa-eye"></i>
                        <span data-i18n="steps.preview">Preview</span>
                    </div>
                    <div class="step" data-step="5">
                        <i class="fas fa-download"></i>
                        <span data-i18n="steps.download">Download</span>
                    </div>
                </div>
            </div>
        `;
    }
    
    // Create toast notification
    static showToast(message, type = 'success', duration = 3000) {
        const existingToast = document.getElementById('toast');
        if (existingToast) existingToast.remove();
        
        const toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = `toast toast-${type}`;
        
        const icon = type === 'success' ? 'check-circle' : 
                    type === 'error' ? 'exclamation-circle' : 'info-circle';
        
        toast.innerHTML = `
            <i class="fas fa-${icon}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Hide toast
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
    
    // Create loading spinner
    static createLoadingSpinner(message = 'Loading...') {
        return `
            <div class="loading-container">
                <div class="magic-animation">
                    <div class="magic-circle">
                        <div class="magic-spark"></div>
                        <div class="magic-spark"></div>
                        <div class="magic-spark"></div>
                        <div class="magic-spark"></div>
                    </div>
                </div>
                <p class="loading-message">${message}</p>
            </div>
        `;
    }
    
    // Create modal dialog
    static createModal(title, content, actions = []) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">${content}</div>
                <div class="modal-actions">
                    ${actions.map(action => 
                        `<button class="btn-${action.type}" onclick="${action.handler}">${action.text}</button>`
                    ).join('')}
                </div>
            </div>
        `;
        
        // Close modal on background click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });
        
        // Close modal on X button
        modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
        
        document.body.appendChild(modal);
        return modal;
    }
}

window.Components = Components;
