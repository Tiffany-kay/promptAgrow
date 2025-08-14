"""
DeepAI Image Generation Service for PromptAgro
Uses DeepAI Text2Image API for reliable agricultural packaging designs
"""

import requests
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any
import os
import base64

class DeepAIImageGenerator:
    def __init__(self, deepai_api_key: str = ""):
        self.deepai_api_key = deepai_api_key
        self.has_deepai = bool(deepai_api_key)
        self.api_url = "https://api.deepai.org/api/text2img"
        
    def create_agricultural_prompt(self, product_data: Dict[str, Any]) -> str:
        """Create professional prompt for agricultural packaging"""
        product_name = product_data.get("productName", "Product")
        colors = product_data.get("colors", ["green", "white"])
        tagline = product_data.get("tagline", "Fresh & Natural")
        emotion = product_data.get("desiredEmotion", "trust")
        platform = product_data.get("salesPlatform", "local-market")
        
        # Color palette
        color_str = " and ".join(colors[:3]) if colors else "green"
        
        # Professional packaging prompt for DeepAI
        prompt = f"""Professional agricultural product packaging design for {product_name}, 
        modern clean style, {color_str} color scheme, premium typography, 
        {tagline}, conveying {emotion}, suitable for {platform}, 
        product photography style, white background, high quality commercial design,
        realistic packaging mockup, professional studio lighting, eco-friendly agricultural branding"""
        
        return prompt.strip().replace('\n', ' ').replace('  ', ' ')
    
    async def generate_packaging_image(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate packaging images using DeepAI Text2Image API
        """
        try:
            print(f"🎨 Generating image with DeepAI API...")
            
            if not self.has_deepai:
                print("⚠️ No DeepAI API key found, using demo mode")
                return await self._create_demo_image(product_data)
            
            # Create the prompt
            prompt = self.create_agricultural_prompt(product_data)
            print(f"📝 Prompt: {prompt[:100]}...")
            
            # Generate image via DeepAI API
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.post(
                    self.api_url,
                    data={'text': prompt},
                    headers={'api-key': self.deepai_api_key},
                    timeout=30
                )
            )
            
            response.raise_for_status()
            result = response.json()
            
            if 'output_url' in result:
                image_url = result['output_url']
                design_id = f"deepai_{uuid.uuid4().hex[:8]}"
                
                print(f"✅ Image generated successfully: {image_url}")
                
                # Optionally download and save the image locally
                await self._save_image_locally(image_url, design_id)
                
                return {
                    "success": True,
                    "design_id": design_id,
                    "image_url": image_url,
                    "generator": "DeepAI Text2Image",
                    "cost": "~$0.005 per image",
                    "prompt_used": prompt
                }
            else:
                print("❌ No output_url in DeepAI response")
                return await self._create_demo_image(product_data)
                
        except Exception as e:
            print(f"❌ DeepAI API error: {str(e)}")
            return await self._create_demo_image(product_data)
    
    async def _save_image_locally(self, image_url: str, design_id: str):
        """Download and save image locally for backup"""
        try:
            loop = asyncio.get_event_loop()
            image_response = await loop.run_in_executor(
                None, 
                lambda: requests.get(image_url, timeout=30)
            )
            
            if image_response.status_code == 200:
                # Create directories
                storage_dir = "storage/designs"
                design_dir = f"{storage_dir}/{design_id}"
                os.makedirs(design_dir, exist_ok=True)
                
                # Save the image
                image_path = f"{design_dir}/{design_id}_deepai.jpg"
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
                
                print(f"📁 Image saved locally: {image_path}")
                
        except Exception as e:
            print(f"Warning: Could not save image locally: {str(e)}")
    
    async def _create_demo_image(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a demo image when DeepAI API is not available"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import base64
            import io
            
            # Create a professional packaging mockup
            img = Image.new('RGB', (1024, 1024), color='white')
            draw = ImageDraw.Draw(img)
            
            # Get product details
            product_name = product_data.get("productName", "Farm Product")
            tagline = product_data.get("tagline", "Fresh & Natural")
            colors = product_data.get("colors", ["green"])
            
            # Color mapping
            color = colors[0] if colors else "green"
            color_map = {
                'green': '#2E7D32', 'blue': '#1976D2', 'red': '#D32F2F',
                'yellow': '#F57C00', 'orange': '#FF9800', 'purple': '#7B1FA2',
                'brown': '#5D4037', 'black': '#424242'
            }
            main_color = color_map.get(color.lower(), '#2E7D32')
            
            # Create gradient background
            for i in range(1024):
                shade = int(255 - (i * 0.05))
                color_val = f'rgb({max(240, shade)},{max(245, shade)},{max(250, shade)})'
                draw.line([(0, i), (1024, i)], fill=color_val)
            
            # Draw main package shape with shadow
            # Shadow
            draw.rectangle([210, 210, 810, 810], fill='#E0E0E0', outline=None)
            # Main package
            draw.rectangle([200, 200, 800, 800], fill=main_color, outline='#333333', width=6)
            
            # Add decorative elements (fix RGBA issue)
            draw.rectangle([220, 220, 780, 320], fill='white', outline=None)
            draw.rectangle([220, 680, 780, 780], fill='white', outline=None)
            
            # Text rendering
            try:
                # Try different font sizes
                font_large = ImageFont.truetype("arial.ttf", 54)
                font_medium = ImageFont.truetype("arial.ttf", 36)
                font_small = ImageFont.truetype("arial.ttf", 24)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Product name (centered)
            bbox = draw.textbbox((0, 0), product_name, font=font_large)
            text_width = bbox[2] - bbox[0]
            text_x = (1024 - text_width) // 2
            
            # Text with outline effect
            for adj in range(-2, 3):
                for adj2 in range(-2, 3):
                    draw.text((text_x + adj, 380 + adj2), product_name, fill='black', font=font_large)
            draw.text((text_x, 380), product_name, fill='white', font=font_large)
            
            # Tagline
            bbox = draw.textbbox((0, 0), tagline, font=font_medium)
            text_width = bbox[2] - bbox[0]
            text_x = (1024 - text_width) // 2
            
            for adj in range(-1, 2):
                for adj2 in range(-1, 2):
                    draw.text((text_x + adj, 480 + adj2), tagline, fill='black', font=font_medium)
            draw.text((text_x, 480), tagline, fill='white', font=font_medium)
            
            # Add "AI Generated" badge
            draw.text((text_x, 580), "🤖 AI Generated Design", fill='white', font=font_small)
            
            # Convert to base64 for inline display
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            design_id = f"demo_{uuid.uuid4().hex[:8]}"
            
            return {
                "success": True,
                "design_id": design_id,
                "image_url": f"data:image/png;base64,{img_str}",
                "generator": "Demo Mode (Enhanced PIL)",
                "cost": "FREE",
                "prompt_used": f"Demo packaging for {product_name} - {tagline}"
            }
            
        except Exception as e:
            print(f"Demo image creation failed: {str(e)}")
            return await self._create_fallback_svg(product_data)
    
    async def _create_fallback_svg(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ultimate fallback - Enhanced SVG placeholder WITH professional advice"""
        import base64
        from .text_advisor import create_smart_packaging_advice, create_concept_summary
        
        design_id = f"fallback_{uuid.uuid4().hex[:8]}"
        product_name = product_data.get("productName", "Product")
        tagline = product_data.get("tagline", "Fresh & Natural")
        colors = product_data.get("colors", ["green"])
        color = colors[0] if colors else "green"
        
        color_map = {
            'green': '#2E7D32', 'blue': '#1976D2', 'red': '#D32F2F',
            'yellow': '#F57C00', 'orange': '#FF9800', 'purple': '#7B1FA2'
        }
        fill_color = color_map.get(color.lower(), '#2E7D32')
        
        svg_content = f'''
        <svg width="1024" height="1024" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{fill_color};stop-opacity:0.9" />
                    <stop offset="100%" style="stop-color:{fill_color};stop-opacity:1" />
                </linearGradient>
                <filter id="shadow">
                    <feDropShadow dx="10" dy="10" stdDeviation="5" flood-opacity="0.3"/>
                </filter>
            </defs>
            <rect width="1024" height="1024" fill="#f8f9fa"/>
            <rect x="200" y="200" width="600" height="600" fill="url(#grad1)" stroke="#333" stroke-width="4" rx="20" filter="url(#shadow)"/>
            <rect x="220" y="220" width="560" height="80" fill="rgba(255,255,255,0.2)" rx="10"/>
            <rect x="220" y="700" width="560" height="80" fill="rgba(255,255,255,0.2)" rx="10"/>
            <text x="500" y="400" font-family="Arial, sans-serif" font-size="48" fill="white" text-anchor="middle" font-weight="bold">{product_name}</text>
            <text x="500" y="460" font-family="Arial, sans-serif" font-size="32" fill="white" text-anchor="middle">{tagline}</text>
            <text x="500" y="580" font-family="Arial, sans-serif" font-size="24" fill="white" text-anchor="middle">💡 With Professional Advice Below</text>
            <text x="500" y="650" font-family="Arial, sans-serif" font-size="20" fill="white" text-anchor="middle">Scroll down for expert design guidance</text>
        </svg>
        '''
        
        # Generate professional advice
        professional_advice = create_smart_packaging_advice(product_data)
        concept_summary = create_concept_summary(product_data)
        
        return {
            "success": True,
            "design_id": design_id,
            "image_url": f"data:image/svg+xml;base64,{base64.b64encode(svg_content.encode()).decode()}",
            "generator": "PKL Smart Designer + Advisor",
            "cost": "FREE (with professional advice!)",
            "has_professional_advice": True,
            "professional_advice": professional_advice,
            "concept_summary": concept_summary,
            "user_message": f"✨ While we upgrade our AI image system, I've created a mockup placeholder AND professional packaging advice for your {product_name}. The advice below is based on design psychology and market research - use it to create amazing packaging!"
        }
