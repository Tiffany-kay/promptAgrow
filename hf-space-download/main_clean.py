import os

# MUST be first - disable all xformers functionality before any imports
os.environ["DISABLE_XFORMERS"] = "1"
os.environ["_DIFFUSERS_DISABLE_XFORMERS"] = "1"
os.environ["XFORMERS_DISABLED"] = "1"

# Set cache directory
os.environ["HF_HOME"] = "/tmp/huggingface_cache"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface_cache"
os.environ["HF_HUB_CACHE"] = "/tmp/huggingface_cache"

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import torch
import uuid
import base64
import io
from PIL import Image

# Import diffusers last with explicit xformers disabling
try:
    from diffusers import StableDiffusionPipeline
except Exception as e:
    print(f"Import error: {e}")
    # Try alternative approach
    import diffusers
    StableDiffusionPipeline = diffusers.StableDiffusionPipeline

# Initialize FastAPI app
app = FastAPI(title="PromptAgro Image Generator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
pipe = None
model_loading = False

def load_model_if_needed():
    """Load model lazily when first request arrives"""
    global pipe, model_loading
    
    if pipe is not None:
        return True
    
    if model_loading:
        return False
    
    model_loading = True
    success = load_model()
    model_loading = False
    return success

def load_model():
    """Load the Stable Diffusion model with proper error handling"""
    global pipe
    
    print("🚀 Loading FASTER Stable Diffusion Model...")
    model_id = "runwayml/stable-diffusion-v1-5"  # MUCH faster & smaller model
    
    try:
        os.makedirs("/tmp/huggingface_cache", exist_ok=True)
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        print(f"📱 Device: {device}, dtype: {torch_dtype}")
        
        # Add safety checker disable for faster loading
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch_dtype,
            cache_dir="/tmp/huggingface_cache",
            local_files_only=False,
            safety_checker=None,              # Disable for speed
            requires_safety_checker=False     # Disable for speed
        )
        
        pipe = pipe.to(device)
        
        print("✅ Using default attention (Windows compatible)")
        print(f"✅ Model Loaded successfully on {device}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        pipe = None
        return False

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "alive",
        "service": "PromptAgro Image Generator",
        "model_loaded": pipe is not None,
        "model_loading": model_loading,
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "model_status": "loaded" if pipe is not None else ("loading" if model_loading else "not_loaded"),
        "torch_dtype": "float16" if torch.cuda.is_available() else "float32",
        "ready_for_requests": pipe is not None,
        "xformers_disabled": True
    }

@app.post("/generate-packaging/")
async def generate_packaging(
    product_name: str = Form(...),
    colors: str = Form("green,yellow"),
    emotion: str = Form("trust"),
    platform: str = Form("farmers-market")
):
    """Generate packaging with PromptAgro-specific prompt engineering"""
    
    if not load_model_if_needed():
        if model_loading:
            raise HTTPException(status_code=503, detail="Model is loading, please wait...")
        else:
            raise HTTPException(status_code=503, detail="Model failed to load. Please check logs.")
    
    prompt = f"""Professional agricultural product packaging design for {product_name}, 
    modern clean style, {colors.replace(',', ' and ')} color scheme, premium typography, 
    conveying {emotion}, suitable for {platform}, product photography style, 
    white background, high quality commercial design, realistic packaging mockup, 
    professional studio lighting, eco-friendly agricultural branding"""
    
    prompt = prompt.strip().replace('\n', ' ').replace('  ', ' ')
    
    print(f"🎨 Generating packaging for: {product_name}")
    
    try:
        image = pipe(
            prompt=prompt,
            width=768,
            height=768,
            num_inference_steps=6,
            guidance_scale=1.5
        ).images[0]
        
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return JSONResponse({
            "success": True,
            "image_data": f"data:image/png;base64,{img_str}",
            "prompt_used": prompt,
            "product_name": product_name,
            "generator": "Stable Diffusion LCM",
            "cost": "FREE"
        })
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting PromptAgro Image Generator (xformers disabled)")
    uvicorn.run(app, host="0.0.0.0", port=7861)  # Use port 7861 to avoid conflicts
