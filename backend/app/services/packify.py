"""
Packify.ai Service Integration
Generates packaging text concepts and design suggestions
"""

import aiohttp
import asyncio
from typing import Dict, Any, List
from app.config import get_settings

settings = get_settings()

class PackifyService:
    def __init__(self):
        self.base_url = "https://api.packify.ai/v1"
        self.api_key = settings.PACKIFY_API_KEY
        self.timeout = 30
    
    async def check_health(self) -> bool:
        """Check if Packify API is accessible"""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                async with session.get(f"{self.base_url}/health", headers=headers) as response:
                    return response.status == 200
        except:
            return False
    
    async def generate_concepts(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate packaging concepts using Packify.ai
        Returns text concepts, style suggestions, and color palettes
        """
        try:
            payload = {
                "product_name": product_data["productName"],
                "tagline": product_data.get("tagline", ""),
                "target_market": product_data.get("salesPlatform", "local-market"),
                "desired_emotion": product_data.get("desiredEmotion", "trust"),
                "product_story": product_data.get("productStory", ""),
                "preferred_colors": product_data.get("preferredColors", []),
                "language": product_data.get("language", "en"),
                "concept_count": 3
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.base_url}/generate-concepts",
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_concepts_response(data)
                    else:
                        # Fallback to mock data if API fails
                        return self._get_fallback_concepts(product_data)
        
        except Exception as e:
            print(f"Packify API error: {e}")
            return self._get_fallback_concepts(product_data)
    
    def _format_concepts_response(self, api_data: Dict) -> Dict[str, Any]:
        """Format Packify API response"""
        return {
            "text_concepts": api_data.get("concepts", []),
            "style_suggestions": api_data.get("styles", []),
            "color_palette": api_data.get("colors", []),
            "emotional_keywords": api_data.get("emotions", []),
            "design_elements": api_data.get("elements", [])
        }
    
    def _get_fallback_concepts(self, product_data: Dict) -> Dict[str, Any]:
        """Fallback concepts when API is unavailable"""
        product_name = product_data.get("productName", "Product")
        emotion = product_data.get("desiredEmotion", "trust")
        
        concepts_map = {
            "trust": [
                f"Premium {product_name} - Trusted Quality",
                f"Farm-Fresh {product_name} - Nature's Best",
                f"Authentic {product_name} - Heritage Crafted"
            ],
            "excitement": [
                f"Bold {product_name} - Adventure Awaits",
                f"Vibrant {product_name} - Energy Unleashed",
                f"Dynamic {product_name} - Pure Excitement"
            ],
            "calm": [
                f"Peaceful {product_name} - Serenity Found",
                f"Gentle {product_name} - Natural Harmony",
                f"Pure {product_name} - Tranquil Essence"
            ]
        }
        
        return {
            "text_concepts": concepts_map.get(emotion, concepts_map["trust"]),
            "style_suggestions": ["Modern Minimalist", "Rustic Artisan", "Premium Elegant"],
            "color_palette": ["#2E7D32", "#FFA726", "#8D6E63", "#5D4037"],
            "emotional_keywords": [emotion.title(), "Quality", "Natural", "Fresh"],
            "design_elements": ["Typography Focus", "Organic Shapes", "Premium Finish"]
        }
