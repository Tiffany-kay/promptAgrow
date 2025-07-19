// Internationalization Module
class I18n {
    constructor() {
        this.currentLanguage = 'en';
        this.translations = {};
        this.fallbackLanguage = 'en';
    }
    
    // Load translation files
    async loadTranslations(language) {
        try {
            const response = await fetch(`i18n/${language}.json`);
            if (!response.ok) throw new Error(`Failed to load ${language} translations`);
            
            this.translations[language] = await response.json();
            return true;
        } catch (error) {
            console.error('Error loading translations:', error);
            return false;
        }
    }
    
    // Set current language
    async setLanguage(language) {
        if (!this.translations[language]) {
            const loaded = await this.loadTranslations(language);
            if (!loaded && language !== this.fallbackLanguage) {
                await this.loadTranslations(this.fallbackLanguage);
                language = this.fallbackLanguage;
            }
        }
        
        this.currentLanguage = language;
        this.updatePageTranslations();
    }
    
    // Get translation by key
    translate(key, params = {}) {
        const keys = key.split('.');
        let translation = this.translations[this.currentLanguage];
        
        // Navigate through nested keys
        for (const k of keys) {
            translation = translation?.[k];
        }
        
        // Fallback to default language
        if (!translation && this.currentLanguage !== this.fallbackLanguage) {
            translation = this.translations[this.fallbackLanguage];
            for (const k of keys) {
                translation = translation?.[k];
            }
        }
        
        // Replace parameters
        if (translation && typeof translation === 'string') {
            Object.keys(params).forEach(param => {
                translation = translation.replace(`{{${param}}}`, params[param]);
            });
        }
        
        return translation || key;
    }
    
    // Update all translations on page
    updatePageTranslations() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.translate(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });
        
        // Update placeholders
        const placeholderElements = document.querySelectorAll('[data-i18n-placeholder]');
        placeholderElements.forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.translate(key);
        });
    }
    
    // Format numbers based on locale
    formatNumber(number, options = {}) {
        const locale = this.getLocale();
        return new Intl.NumberFormat(locale, options).format(number);
    }
    
    // Format dates based on locale
    formatDate(date, options = {}) {
        const locale = this.getLocale();
        return new Intl.DateTimeFormat(locale, options).format(date);
    }
    
    // Get locale code from language
    getLocale() {
        const localeMap = {
            'en': 'en-US',
            'sw': 'sw-TZ',
            'fr': 'fr-FR'
        };
        return localeMap[this.currentLanguage] || 'en-US';
    }
}

// Create global i18n instance
window.i18n = new I18n();
