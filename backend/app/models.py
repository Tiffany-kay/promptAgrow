"""
Simplified Pydantic models for PromptAgro API
No complex dependencies
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    services: Dict[str, bool]

class GenerateResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class CustomizationData(BaseModel):
    colors: Optional[List[str]] = []
    text_changes: Optional[Dict[str, str]] = {}
    style_preferences: Optional[Dict[str, str]] = {}

class RegenerateRequest(BaseModel):
    designId: str
    customizations: CustomizationData

class SaveDesignRequest(BaseModel):
    designId: str
    userEmail: str  # Simple string instead of EmailStr
    designName: str

class ConceptResponse(BaseModel):
    text_concepts: List[str]
    style_suggestions: List[str]
    color_palette: List[str]
    emotional_keywords: List[str]

class MockupData(BaseModel):
    image_path: str
    processing_time: float
    dimensions: Dict[str, int]
    quality_score: Optional[float] = None
