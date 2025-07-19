# PromptAgro Backend Setup & Testing Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start Backend Server
```bash
# Windows
start.bat

# PowerShell
.\start.ps1

# Manual
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 API Endpoints

### Health Check
```
GET /api/health
```

### Main Generation
```
POST /api/generate
Content-Type: multipart/form-data

Fields:
- image: File (required)
- productName: string (required)
- tagline: string
- preferredColors: JSON array
- salesPlatform: string
- desiredEmotion: string
- productStory: string
- language: string
```

### Design Regeneration
```
POST /api/regenerate
Content-Type: application/json

{
  "designId": "design_12345",
  "customizations": {
    "colors": ["#FF5722", "#4CAF50"],
    "text_changes": {"tagline": "New tagline"},
    "style_preferences": {"style": "modern"}
  }
}
```

### Save Design
```
POST /api/save-design
Content-Type: application/json

{
  "designId": "design_12345",
  "userEmail": "user@example.com",
  "designName": "My Awesome Design"
}
```

### Test Upload
```
POST /api/test-upload
Content-Type: multipart/form-data

Fields:
- image: File
```

## 🔧 Testing Commands

### Test Health Endpoint
```bash
curl http://localhost:8000/api/health
```

### Test File Upload
```bash
curl -X POST -F "image=@sample.jpg" http://localhost:8000/api/test-upload
```

### Test Full Generation
```bash
curl -X POST \
  -F "image=@sample.jpg" \
  -F "productName=Premium Coffee" \
  -F "tagline=Ethically Sourced" \
  -F "preferredColors=[\"#8B4513\",\"#F4A460\"]" \
  -F "salesPlatform=premium-retail" \
  -F "desiredEmotion=trust" \
  -F "language=en" \
  http://localhost:8000/api/generate
```

## 📁 Directory Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── config.py        # Settings
│   ├── routes.py        # API endpoints
│   ├── models.py        # Pydantic models
│   ├── utils.py         # Utilities
│   └── services/
│       ├── __init__.py
│       ├── packify.py   # Packify.ai integration
│       ├── gemini.py    # Gemini Vision integration
│       └── storage.py   # File storage
├── storage/             # Generated at runtime
│   ├── uploads/
│   ├── designs/
│   └── mockups/
├── static/              # Static files
├── requirements.txt
├── .env.example
├── start.bat
└── start.ps1
```

## 🔍 Troubleshooting

### Backend Won't Start
1. Check Python version (3.8+)
2. Install dependencies: `pip install -r requirements.txt`
3. Check port 8000 is available

### API Key Errors
1. Copy `.env.example` to `.env`
2. Add your actual API keys:
   - PACKIFY_API_KEY
   - GEMINI_API_KEY

### File Upload Issues
1. Check file size < 10MB
2. Ensure image format is supported
3. Verify storage directory permissions

### CORS Errors
1. Check CORS_ORIGINS in .env
2. Add your frontend URL to allowed origins

## 📊 API Documentation
Visit http://localhost:8000/docs for interactive API documentation

## 🔄 Integration Status
✅ Backend structure complete
✅ All required endpoints implemented
✅ File upload handling
✅ AI service integrations prepared
✅ Error handling & validation
✅ Static file serving
✅ CORS configuration

The backend is now fully integrated with your frontend and ready for testing!
