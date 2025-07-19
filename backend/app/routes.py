"""
API Routes for PromptAgro Backend
Using our own AI instead of external services
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import json
import uuid
import asyncio
from datetime import datetime

from app.models import (
    GenerateResponse, 
    RegenerateRequest, 
    SaveDesignRequest,
    HealthResponse
)
from app.services.promptagro_ai import PromptAgroAI
from app.services.storage import StorageService
from app.utils_simple import validate_image, create_pdf_report
from app.config import settings

router = APIRouter()

# Initialize services with our own AI
promptagro_ai = PromptAgroAI(settings.GOOGLE_AI_API_KEY)
storage_service = StorageService()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        services={
            "promptagro_ai": await promptagro_ai.check_health(),
            "storage": await storage_service.check_health()
        }
    )

@router.post("/generate", response_model=GenerateResponse)
async def generate_packaging(
    image: UploadFile = File(...),
    productName: str = Form(...),
    tagline: str = Form(""),
    preferredColors: str = Form("[]"),
    salesPlatform: str = Form("local-market"),
    desiredEmotion: str = Form("trust"),
    productStory: str = Form(""),
    language: str = Form("en")
):
    """
    Main packaging generation endpoint using our own AI
    """
    try:
        # Validate image
        if not validate_image(image):
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Parse preferred colors
        try:
            colors = json.loads(preferredColors)
        except json.JSONDecodeError:
            colors = []
        
        # Create design ID
        design_id = f"design_{uuid.uuid4().hex[:8]}"
        
        # Save uploaded image
        image_path = await storage_service.save_upload(image, design_id)
        
        # Step 1: Generate packaging concepts with our AI
        concepts = await promptagro_ai.generate_packaging_concepts({
            "productName": productName,
            "tagline": tagline,
            "preferredColors": colors,
            "salesPlatform": salesPlatform,
            "desiredEmotion": desiredEmotion,
            "productStory": productStory,
            "language": language
        })
        
        # Step 2: Generate mockup with our AI
        mockup_data = await promptagro_ai.generate_packaging_mockup(
            image_path=image_path,
            concepts=concepts,
            product_data={
                "productName": productName,
                "tagline": tagline,
                "colors": colors
            }
        )
        
        # Step 3: Create design report
        report_path = await create_pdf_report(
            design_id=design_id,
            mockup_data=mockup_data,
            concepts=concepts,
            product_data={
                "productName": productName,
                "tagline": tagline,
                "productStory": productStory
            }
        )
        
        # Step 4: Generate public URLs
        mockup_url = await storage_service.get_public_url(mockup_data["image_path"])
        report_url = await storage_service.get_public_url(report_path)
        
        return GenerateResponse(
            success=True,
            data={
                "designId": design_id,
                "mockupUrl": mockup_url,
                "reportUrl": report_url,
                "concepts": concepts["text_concepts"],
                "stylesSuggestions": concepts["style_suggestions"],
                "colorPalette": concepts["color_palette"],
                "processingTime": mockup_data.get("processing_time", 0),
                "aiConfidence": mockup_data.get("ai_confidence", 0.85)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@router.post("/regenerate")
async def regenerate_design(request: RegenerateRequest):
    """
    Design customization endpoint using our AI
    """
    try:
        # Validate design exists
        design_exists = await storage_service.design_exists(request.designId)
        if not design_exists:
            raise HTTPException(status_code=404, detail="Design not found")
        
        # Apply customizations with our AI
        updated_mockup = await promptagro_ai.generate_packaging_mockup(
            image_path=f"storage/uploads/{request.designId}_original.jpg",
            concepts={
                "text_concepts": ["Updated Design"],
                "style_suggestions": list(request.customizations.style_preferences.values()),
                "color_palette": request.customizations.colors or ["#2E7D32"]
            },
            product_data={"productName": "Updated Product"}
        )
        
        # Generate new public URL
        mockup_url = await storage_service.get_public_url(updated_mockup["image_path"])
        
        return {
            "success": True,
            "data": {
                "mockupUrl": mockup_url,
                "designId": request.designId,
                "processingTime": updated_mockup.get("processing_time", 0),
                "aiConfidence": updated_mockup.get("ai_confidence", 0.85)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Regeneration failed: {str(e)}")

@router.post("/save-design")
async def save_design(request: SaveDesignRequest):
    """Save design to user account"""
    try:
        # Generate saved design ID
        saved_design_id = f"saved_{uuid.uuid4().hex[:8]}"
        
        # Save design metadata
        design_data = {
            "savedDesignId": saved_design_id,
            "originalDesignId": request.designId,
            "userEmail": request.userEmail,
            "designName": request.designName,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Store in database/storage
        await storage_service.save_design_metadata(design_data)
        
        return {
            "success": True,
            "savedDesignId": saved_design_id,
            "message": "Design saved successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Save failed: {str(e)}")

@router.post("/test-upload")
async def test_upload(image: UploadFile = File(...)):
    """Testing endpoint for file upload"""
    try:
        # Basic file validation
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Check file size
        contents = await image.read()
        if len(contents) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File too large")
        
        return {
            "success": True,
            "message": "File upload test successful",
            "filename": image.filename,
            "size": len(contents),
            "contentType": image.content_type
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload test failed: {str(e)}")

@router.get("/sample-design")
async def get_sample_design():
    """Return sample design for frontend testing"""
    return {
        "success": True,
        "data": {
            "designId": "sample_design_123",
            "mockupUrl": "/static/sample-mockup.jpg",
            "reportUrl": "/static/sample-design.txt",
            "concepts": [
                "Premium Farm Fresh - Nature's Best Quality",
                "Artisan Organic - Traditionally Crafted",
                "Pure Natural - Sustainably Grown"
            ],
            "stylesSuggestions": ["Modern Organic", "Rustic Premium", "Clean Natural"],
            "colorPalette": ["#2E7D32", "#8BC34A", "#FFC107", "#795548"],
            "processingTime": 2.1,
            "aiConfidence": 0.88
        }
    }
