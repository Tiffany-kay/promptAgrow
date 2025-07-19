"""
Configuration settings for PromptAgro Backend
"""

import os
from typing import List

class Settings:
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    STATIC_DIR: str = "static"
    
    # AI Service Configuration
    PACKIFY_API_KEY: str = os.getenv("PACKIFY_API_KEY", "")
    GOOGLE_AI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AIzaSyDkfvNr22S_T6t77cQbdZq7tbwIiZ2CD2g")
    
    # Cloud Storage Configuration  
    CLOUD_STORAGE_BUCKET: str = os.getenv("CLOUD_STORAGE_BUCKET", "promptagro-designs")
    
    # Database Configuration (if needed)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./promptagro.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")

# Create settings instance
settings = Settings()
