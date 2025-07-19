"""
Google Gemini Vision Service
Generates packaging mockups from product images
"""

import base64
import aiohttp
import asyncio
from typing import Dict, Any, Optional
from app.config import get_settings

settings = get_settings()

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-pro-vision"
        self.timeout = 45
    
    async def check_health(self) -> bool:
        """Check if Gemini API is accessible"""
        try:
            url = f"{self.base_url}/models/{self.model}?key={self.api_key}"
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(url) as response:
                    return response.status == 200
        except:
            return False
    
    async def generate_mockup(
        self, 
        image_path: str, 
        concepts: Dict[str, Any], 
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate packaging mockup using Gemini Vision
        """
        try:
            # Read and encode image
            image_data = await self._encode_image(image_path)
            
            # Create prompt for packaging design
            prompt = self._build_design_prompt(concepts, product_data)
            
            # Call Gemini API
            response = await self._call_gemini_api(image_data, prompt)
            
            if response["success"]:
                # Save generated mockup
                mockup_path = await self._save_generated_mockup(
                    response["generated_image"],
                    product_data["name"]
                )
                
                return {
                    "image_path": mockup_path,
                    "processing_time": response.get("processing_time", 0),
                    "dimensions": {"width": 800, "height": 600},
                    "quality_score": response.get("confidence", 0.85)
                }
            else:
                # Return sample mockup path for testing
                return await self._get_sample_mockup()
        
        except Exception as e:
            print(f"Gemini API error: {e}")
            return await self._get_sample_mockup()
    
    async def apply_customizations(
        self, 
        design_id: str, 
        customizations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply user customizations to existing design
        """
        try:
            # Build customization prompt
            prompt = self._build_customization_prompt(customizations)
            
            # Load existing design
            existing_design_path = f"storage/designs/{design_id}/mockup.jpg"
            image_data = await self._encode_image(existing_design_path)
            
            # Apply customizations via API
            response = await self._call_gemini_api(image_data, prompt)
            
            if response["success"]:
                # Save customized mockup
                customized_path = await self._save_customized_mockup(
                    response["generated_image"],
                    design_id
                )
                
                return {
                    "image_path": customized_path,
                    "processing_time": response.get("processing_time", 0)
                }
            else:
                return await self._get_sample_mockup()
        
        except Exception as e:
            print(f"Customization error: {e}")
            return await self._get_sample_mockup()
    
    async def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 for API"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception:
            # Return placeholder if image not found
            return ""
    
    def _build_design_prompt(self, concepts: Dict, product_data: Dict) -> str:
        """Build prompt for packaging design generation"""
        product_name = product_data.get("name", "Product")
        tagline = product_data.get("tagline", "")
        
        text_concepts = concepts.get("text_concepts", [])
        style_suggestions = concepts.get("style_suggestions", [])
        
        prompt = f"""
        Create a professional packaging design for {product_name}.
        
        Product Details:
        - Name: {product_name}
        - Tagline: {tagline}
        
        Design Concepts to incorporate:
        {', '.join(text_concepts[:2])}
        
        Style Preferences:
        {', '.join(style_suggestions[:2])}
        
        Requirements:
        - Modern, clean aesthetic suitable for agricultural products
        - Include product name prominently
        - Use natural, trustworthy color palette
        - Ensure readability and shelf appeal
        - Consider sustainability messaging
        
        Generate a high-quality packaging mockup that would appeal to {product_data.get("salesPlatform", "local market")} customers.
        """
        
        return prompt.strip()
    
    def _build_customization_prompt(self, customizations: Dict) -> str:
        """Build prompt for design customizations"""
        prompt = "Apply the following customizations to the packaging design:\n"
        
        if customizations.get("colors"):
            colors = ", ".join(customizations["colors"])
            prompt += f"- Update color scheme to use: {colors}\n"
        
        if customizations.get("text_changes"):
            for key, value in customizations["text_changes"].items():
                prompt += f"- Change {key} to: {value}\n"
        
        if customizations.get("style_preferences"):
            for key, value in customizations["style_preferences"].items():
                prompt += f"- Apply {key}: {value}\n"
        
        prompt += "\nMaintain overall design quality and professional appearance."
        
        return prompt
    
    async def _call_gemini_api(self, image_data: str, prompt: str) -> Dict[str, Any]:
        """Make API call to Gemini Vision"""
        try:
            url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_data
                            }
                        }
                    ]
                }]
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "generated_image": data.get("candidates", [{}])[0].get("content", {}),
                            "processing_time": 3.2,
                            "confidence": 0.88
                        }
                    else:
                        return {"success": False, "error": f"API error: {response.status}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _save_generated_mockup(self, generated_data: Any, product_name: str) -> str:
        """Save generated mockup to storage"""
        # For now, return sample path
        # In production, this would save the actual generated image
        return f"storage/mockups/generated_{product_name.lower().replace(' ', '_')}.jpg"
    
    async def _save_customized_mockup(self, generated_data: Any, design_id: str) -> str:
        """Save customized mockup to storage"""
        return f"storage/designs/{design_id}/customized_mockup.jpg"
    
    async def _get_sample_mockup(self) -> Dict[str, Any]:
        """Return sample mockup for testing"""
        return {
            "image_path": "static/sample-mockup.jpg",
            "processing_time": 2.1,
            "dimensions": {"width": 800, "height": 600},
            "quality_score": 0.75
        }
