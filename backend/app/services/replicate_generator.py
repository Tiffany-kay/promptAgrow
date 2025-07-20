"""
Replicate AI Image Generation Service for PromptAgro
Uses Stability AI SDXL via Replicate API for high-quality agricultural packaging designs
"""

import replicate
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any
import os

class ReplicateImageGenerator:
    def __init__(self, replicate_api_key: str = ""):
        self.replicate_api_key = replicate_api_key
        self.has_replicate = bool(replicate_api_key)
        
        # Initialize Replicate client
        if self.has_replicate:
            self.client = replicate.Client(api_token=replicate_api_key)
        else:
            self.client = None
        
    def create_agricultural_prompt(self, product_data: Dict[str, Any]) -> str:
        """Create professional prompt for agricultural packaging"""
        product_name = product_data.get("productName", "Product")
        colors = product_data.get("colors", ["green", "white"])
        tagline = product_data.get("tagline", "Fresh & Natural")
        emotion = product_data.get("desiredEmotion", "trust")
        platform = product_data.get("salesPlatform", "local-market")
        
        # Color palette
        color_str = " and ".join(colors[:3])
        
        # Professional packaging prompt for Stability AI SDXL
        prompt = f"""Professional agricultural product packaging design for {product_name}, 
        modern minimalist style, {color_str} color scheme, clean typography, 
        premium quality feel, {tagline}, conveying {emotion}, 
        suitable for {platform}, product photography style, 
        white background, high resolution, commercial grade design,
        photorealistic packaging mockup, studio lighting, eco-friendly design"""
        
        return prompt.strip().replace('\n', ' ').replace('  ', ' ')
    
    async def generate_packaging_image(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate packaging images using Stability AI SDXL via Replicate
        """
        try:
            print(f"🎨 Generating image with Replicate API...")
            
            if not self.has_replicate or not self.client:
                print("⚠️ No Replicate API key found, using demo mode")
                return await self._create_demo_image(product_data)
            
            # Create the prompt
            prompt = self.create_agricultural_prompt(product_data)
            print(f"📝 Prompt: {prompt}")
            
            # Generate image via Replicate API
            loop = asyncio.get_event_loop()
            output = await loop.run_in_executor(
                None, 
                lambda: self.client.run(
                    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                    input={
                        "prompt": prompt,
                        "width": 1024,
                        "height": 1024,
                        "num_outputs": 1,
                        "scheduler": "K_EULER",
                        "num_inference_steps": 20,
                        "guidance_scale": 7.5,
                        "prompt_strength": 0.8,
                        "refine": "expert_ensemble_refiner",
                        "high_noise_frac": 0.8
                    }
                )
            )
            
            if output and len(output) > 0:
                image_url = output[0]  # Replicate returns a list of URLs
                design_id = f"replicate_{uuid.uuid4().hex[:8]}"
                
                print(f"✅ Image generated successfully: {image_url}")
                
                return {
                    "success": True,
                    "design_id": design_id,
                    "image_url": image_url,
                    "generator": "Stability AI SDXL (Replicate)",
                    "cost": "~$0.0012 per image",
                    "prompt_used": prompt
                }
            else:
                print("❌ No output from Replicate")
                return await self._create_demo_image(product_data)
                
        except Exception as e:
            print(f"❌ Replicate API error: {str(e)}")
            return await self._create_demo_image(product_data)
    
    async def _create_demo_image(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a demo image when Replicate API is not available"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import base64
            import io
            
            # Create a simple packaging mockup
            img = Image.new('RGB', (1024, 1024), color='white')
            draw = ImageDraw.Draw(img)
            
            # Draw a simple package design
            colors = product_data.get("colors", ["green"])
            box_color = colors[0] if colors else "green"
            
            # Color mapping
            if not box_color.startswith('#'):
                color_map = {
                    'green': '#4CAF50', 'blue': '#2196F3', 'red': '#F44336',
                    'yellow': '#FFEB3B', 'orange': '#FF9800', 'purple': '#9C27B0',
                    'brown': '#8D6E63', 'black': '#424242'
                }
                box_color = color_map.get(box_color.lower(), '#4CAF50')
            
            # Draw package shape - more sophisticated design
            # Background gradient effect
            for i in range(100):
                shade = int(240 - i * 0.5)
                draw.rectangle([i*10, i*10, 1024-i*10, 1024-i*10], 
                             outline=f'rgb({shade},{shade},{shade})')
            
            # Main package rectangle
            draw.rectangle([200, 200, 800, 800], fill=box_color, outline='black', width=4)
            
            # Add product name
            product_name = product_data.get("productName", "Farm Product")
            tagline = product_data.get("tagline", "Fresh & Natural")
            
            try:
                # Try different font sizes
                font_large = ImageFont.truetype("arial.ttf", 48)
                font_medium = ImageFont.truetype("arial.ttf", 32)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                
            # Calculate text positions
            bbox = draw.textbbox((0, 0), product_name, font=font_large)
            text_width = bbox[2] - bbox[0]
            text_x = (1024 - text_width) // 2
            
            # Product name
            draw.text((text_x, 350), product_name, fill='white', font=font_large)
            
            # Tagline
            bbox = draw.textbbox((0, 0), tagline, font=font_medium)
            text_width = bbox[2] - bbox[0]
            text_x = (1024 - text_width) // 2
            draw.text((text_x, 450), tagline, fill='white', font=font_medium)
            
            # Add "AI Generated" watermark
            draw.text((text_x, 600), "🤖 AI Generated Design", fill='white', font=font_medium)
            
            # Convert to base64 for inline display
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            design_id = f"demo_{uuid.uuid4().hex[:8]}"
            
            return {
                "success": True,
                "design_id": design_id,
                "image_url": f"data:image/png;base64,{img_str}",
                "generator": "Demo Mode (Local PIL)",
                "cost": "FREE",
                "prompt_used": f"Demo packaging for {product_name}"
            }
            
        except Exception as e:
            print(f"Demo image creation failed: {str(e)}")
            return await self._create_fallback_svg(product_data)
    
    async def _create_fallback_svg(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ultimate fallback - SVG placeholder"""
        import base64
        
        design_id = f"fallback_{uuid.uuid4().hex[:8]}"
        product_name = product_data.get("productName", "Product")
        tagline = product_data.get("tagline", "Fresh & Natural")
        colors = product_data.get("colors", ["green"])
        color = colors[0] if colors else "green"
        
        color_map = {
            'green': '#4CAF50', 'blue': '#2196F3', 'red': '#F44336',
            'yellow': '#FFEB3B', 'orange': '#FF9800', 'purple': '#9C27B0'
        }
        fill_color = color_map.get(color.lower(), '#4CAF50')
        
        svg_content = f'''
        <svg width="1024" height="1024" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{fill_color};stop-opacity:0.8" />
                    <stop offset="100%" style="stop-color:{fill_color};stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="1024" height="1024" fill="#f8f9fa"/>
            <rect x="200" y="200" width="600" height="600" fill="url(#grad1)" stroke="black" stroke-width="4" rx="20"/>
            <text x="512" y="400" font-family="Arial, sans-serif" font-size="48" fill="white" text-anchor="middle" font-weight="bold">{product_name}</text>
            <text x="512" y="480" font-family="Arial, sans-serif" font-size="32" fill="white" text-anchor="middle">{tagline}</text>
            <text x="512" y="650" font-family="Arial, sans-serif" font-size="24" fill="white" text-anchor="middle">🤖 AI Generated Design</text>
        </svg>
        '''
        
        return {
            "success": True,
            "design_id": design_id,
            "image_url": f"data:image/svg+xml;base64,{base64.b64encode(svg_content.encode()).decode()}",
            "generator": "SVG Fallback",
            "cost": "FREE"
        }
