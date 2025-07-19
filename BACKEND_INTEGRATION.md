# Backend Integration Instructions for PromptAgro Frontend

## 🎯 Overview
The frontend is ready for integration. Backend needs to provide REST API endpoints that match the existing frontend data flow.

## 📡 Required API Endpoints

### 1. **POST /api/generate** - Main Packaging Generation
**Purpose**: Process uploaded image + form data, generate AI packaging design

**Request Format**: `multipart/form-data`
```json
{
  "image": "file (uploaded product photo)",
  "productName": "string",
  "tagline": "string", 
  "preferredColors": ["#color1", "#color2"],
  "salesPlatform": "local-market|online|wholesale|retail|farmers-market",
  "desiredEmotion": "trust|premium|natural|traditional|modern|family",
  "productStory": "string (max 500 chars)",
  "language": "en|sw|fr"
}
```

**Response Format**: `application/json`
```json
{
  "success": true,
  "data": {
    "mockupUrl": "https://storage.googleapis.com/bucket/mockup-12345.jpg",
    "pdfUrl": "https://storage.googleapis.com/bucket/design-12345.pdf",
    "designId": "design_67890",
    "concepts": [
      "Fresh & Natural Branding",
      "Premium Artisan Look", 
      "Traditional Heritage Style"
    ],
    "processingTime": 3.2
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Image processing failed",
  "code": "PROCESSING_ERROR"
}
```

### 2. **POST /api/regenerate** - Customize Design
**Purpose**: Apply user customizations to existing design

**Request Format**: `application/json`
```json
{
  "designId": "design_67890",
  "customizations": {
    "brightness": 120,
    "contrast": 110,
    "saturation": 95,
    "fontStyle": "serif|script|bold-sans",
    "layout": "top-label|wrap-around|sticker"
  },
  "language": "en|sw|fr"
}
```

**Response Format**: Same as `/api/generate`

### 3. **POST /api/save-design** - Save to User Account
**Purpose**: Save design to user's collection

**Request Format**: `application/json`
```json
{
  "designId": "design_67890",
  "userEmail": "farmer@example.com", 
  "designName": "My Honey Package"
}
```

**Response Format**:
```json
{
  "success": true,
  "savedDesignId": "saved_12345"
}
```

## 🔧 Integration Points in Frontend

### 1. **API Base URL Configuration**
**File**: `frontend/js/api.js`
**Change Line 4**:
```javascript
// FROM:
this.baseURL = '/api'; 

// TO:
this.baseURL = 'https://your-backend-domain.com/api';
// OR for local development:
this.baseURL = 'http://localhost:8080/api';
```

### 2. **Remove Mock Responses**
**File**: `frontend/js/api.js`
**Lines 28-42**: Replace mock `setTimeout` with actual fetch calls:

```javascript
// REPLACE THIS MOCK:
return new Promise((resolve) => {
    setTimeout(() => {
        resolve({
            success: true,
            mockupUrl: 'assets/sample-mockup.jpg',
            // ... mock data
        });
    }, 3000);
});

// WITH ACTUAL API CALL:
const response = await this.request('/generate', {
    method: 'POST',
    body: formData
});
return response;
```

### 3. **Form Data Mapping**
**File**: `frontend/js/app.js`
**Function**: `handleImageUpload()` 
**The frontend already collects data in this format**:
```javascript
// Frontend state.form object matches backend expectations:
{
    image: File,              // → Direct file upload
    productName: "string",    // → productName
    tagline: "string",        // → tagline  
    preferredColors: [],      // → preferredColors array
    salesPlatform: "string",  // → salesPlatform enum
    desiredEmotion: "string", // → desiredEmotion enum
    productStory: "string"    // → productStory
}
```

## 🌐 CORS Configuration Required
Backend must allow these origins:
```
http://localhost:8000
http://localhost:3000
https://your-frontend-domain.com
```

## 📁 File Upload Handling
- **Max file size**: 10MB
- **Accepted formats**: `image/jpeg`, `image/png`, `image/webp`
- **Image processing**: Resize to max 1024x1024 for AI processing
- **Storage**: Return public URLs for generated assets

## 🤖 AI Service Integration Flow

### Packify.ai Integration
```python
# services/packify.py
def generate_concepts(product_data):
    # Call Packify.ai with form data
    # Return packaging concepts and text layouts
```

### Gemini Vision Integration  
```python
# services/gemini.py
def generate_mockup(image_file, concepts, customizations):
    # Call Gemini Vision API
    # Return generated mockup image URL
```

### PDF Generation
```python
# utils.py
def create_pdf_report(mockup_url, concepts, product_data):
    # Generate branded PDF with design guide
    # Return PDF download URL
```

## 🌍 Multilingual Support
Backend should return translated labels based on `language` parameter:

**English Response**:
```json
{
  "concepts": ["Fresh & Natural", "Premium Look"],
  "messages": {
    "processing": "Creating your design...",
    "complete": "Design ready!"
  }
}
```

**Swahili Response**: 
```json
{
  "concepts": ["Asili na Mazingira", "Muonekano wa Hali ya Juu"],
  "messages": {
    "processing": "Kuunda muundo wako...",
    "complete": "Muundo umemaliza!"
  }
}
```

## ⚡ Performance Requirements
- **Image upload**: < 30 seconds end-to-end
- **Regeneration**: < 10 seconds  
- **File storage**: Use cloud storage (GCP/AWS) for generated assets
- **Caching**: Cache common design patterns

## 🔒 Security Considerations
- **File validation**: Check file types and scan for malware
- **Rate limiting**: Max 5 generations per user per hour
- **Input sanitization**: Clean all text inputs
- **HTTPS only**: All API calls must use HTTPS in production

## 📝 Environment Variables Backend Needs
```bash
PACKIFY_AI_API_KEY=your_packify_key
GOOGLE_AI_API_KEY=your_gemini_key  
CLOUD_STORAGE_BUCKET=your_bucket_name
CORS_ORIGINS=http://localhost:8000,https://yourdomain.com
MAX_FILE_SIZE=10485760
```

## 🧪 Testing Endpoints
Provide these test endpoints:
- **GET /api/health** - Health check
- **POST /api/test-upload** - Test file upload without AI processing
- **GET /api/sample-design** - Return sample design for frontend testing

## 🎯 Priority Implementation Order
1. **Basic file upload** (POST /api/generate) 
2. **Packify.ai integration** (text concepts)
3. **Image generation** (Gemini Vision)
4. **PDF generation** (design report)
5. **Customization** (POST /api/regenerate)
6. **User accounts** (POST /api/save-design)

This matches exactly what the frontend expects! Once you implement these endpoints, just change the `baseURL` in `api.js` and remove the mock responses. 🚀
