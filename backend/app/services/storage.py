"""
Storage Service for PromptAgro
Handles file uploads, cloud storage, and design management
"""

import os
import uuid
import json
import aiofiles
from typing import Optional, Dict, Any
from fastapi import UploadFile
from datetime import datetime
from app.config import settings

class StorageService:
    def __init__(self):
        self.upload_dir = "storage/uploads"
        self.designs_dir = "storage/designs"
        self.mockups_dir = "storage/mockups"
        self.metadata_file = "storage/design_metadata.json"
        
        # Create directories if they don't exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create storage directories"""
        for directory in [self.upload_dir, self.designs_dir, self.mockups_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Create metadata file if it doesn't exist
        if not os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'w') as f:
                json.dump({}, f)
    
    async def check_health(self) -> bool:
        """Check if storage system is accessible"""
        try:
            # Test write access
            test_file = f"{self.upload_dir}/health_check.txt"
            async with aiofiles.open(test_file, 'w') as f:
                await f.write("health check")
            
            # Clean up test file
            if os.path.exists(test_file):
                os.remove(test_file)
            
            return True
        except:
            return False
    
    async def save_upload(self, file: UploadFile, design_id: str) -> str:
        """
        Save uploaded file to storage
        Returns the file path
        """
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{design_id}_original{file_extension}"
        file_path = os.path.join(self.upload_dir, filename)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return file_path
    
    async def get_public_url(self, file_path: str) -> str:
        """
        Generate public URL for file
        In production, this would generate signed URLs for cloud storage
        """
        # Convert local path to URL path
        if file_path.startswith("storage/"):
            return f"/static/{file_path}"
        elif file_path.startswith("static/"):
            return f"/{file_path}"
        else:
            return f"/static/{os.path.basename(file_path)}"
    
    async def design_exists(self, design_id: str) -> bool:
        """Check if design exists in storage"""
        design_dir = os.path.join(self.designs_dir, design_id)
        return os.path.exists(design_dir)
    
    async def save_design_metadata(self, design_data: Dict[str, Any]) -> bool:
        """Save design metadata to storage"""
        try:
            # Load existing metadata
            async with aiofiles.open(self.metadata_file, 'r') as f:
                content = await f.read()
                metadata = json.loads(content) if content else {}
            
            # Add new design
            metadata[design_data["savedDesignId"]] = design_data
            
            # Save updated metadata
            async with aiofiles.open(self.metadata_file, 'w') as f:
                await f.write(json.dumps(metadata, indent=2))
            
            return True
        except Exception as e:
            print(f"Metadata save error: {e}")
            return False
    
    async def get_design_metadata(self, design_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve design metadata"""
        try:
            async with aiofiles.open(self.metadata_file, 'r') as f:
                content = await f.read()
                metadata = json.loads(content) if content else {}
                return metadata.get(design_id)
        except:
            return None
    
    async def list_user_designs(self, user_email: str) -> list:
        """List all designs for a user"""
        try:
            async with aiofiles.open(self.metadata_file, 'r') as f:
                content = await f.read()
                metadata = json.loads(content) if content else {}
            
            user_designs = []
            for design_id, data in metadata.items():
                if data.get("userEmail") == user_email:
                    user_designs.append(data)
            
            # Sort by timestamp (newest first)
            user_designs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            return user_designs
        except:
            return []
    
    async def create_design_directory(self, design_id: str) -> str:
        """Create directory for design files"""
        design_dir = os.path.join(self.designs_dir, design_id)
        os.makedirs(design_dir, exist_ok=True)
        return design_dir
    
    async def save_mockup(self, design_id: str, mockup_data: bytes) -> str:
        """Save generated mockup"""
        design_dir = await self.create_design_directory(design_id)
        mockup_path = os.path.join(design_dir, "mockup.jpg")
        
        async with aiofiles.open(mockup_path, 'wb') as f:
            await f.write(mockup_data)
        
        return mockup_path
    
    async def cleanup_old_files(self, days: int = 30):
        """Clean up files older than specified days"""
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        for directory in [self.upload_dir, self.designs_dir, self.mockups_dir]:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.getmtime(file_path) < cutoff_time:
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            import shutil
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f"Cleanup error: {e}")
    
    async def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage usage statistics"""
        stats = {
            "total_uploads": 0,
            "total_designs": 0,
            "storage_used_mb": 0
        }
        
        try:
            # Count uploads
            stats["total_uploads"] = len(os.listdir(self.upload_dir))
            
            # Count designs
            stats["total_designs"] = len(os.listdir(self.designs_dir))
            
            # Calculate storage usage
            total_size = 0
            for directory in [self.upload_dir, self.designs_dir, self.mockups_dir]:
                for dirpath, dirnames, filenames in os.walk(directory):
                    for filename in filenames:
                        file_path = os.path.join(dirpath, filename)
                        total_size += os.path.getsize(file_path)
            
            stats["storage_used_mb"] = round(total_size / (1024 * 1024), 2)
            
        except Exception as e:
            print(f"Stats calculation error: {e}")
        
        return stats
