import os

# Disable xformers to avoid Windows compatibility issues (MUST be before diffusers import)
os.environ["DISABLE_XFORMERS"] = "1"
os.environ["_DIFFUSERS_DISABLE_XFORMERS"] = "1"

# Set cache directory to a writable location
os.environ["HF_HOME"] = "/tmp/huggingface_cache"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface_cache"
os.environ["HF_HUB_CACHE"] = "/tmp/huggingface_cache"

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from diffusers import StableDiffusionPipeline
import torch
import uuid
import base64
import io
from PIL import Image

# Initialize FastAPI app
app = FastAPI(title="PromptAgro Image Generator API")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable for the pipeline
pipe = None
model_loading = False

def load_model_if_needed():
    """Load model lazily when first request arrives"""
    global pipe, model_loading
    
    if pipe is not None:
        return True
    
    if model_loading:
        return False  # Already loading, wait
    
    model_loading = True
    success = load_model()
    model_loading = False
    return success

def load_model():
    """Load the Stable Diffusion model with proper error handling"""
    global pipe
    
    print("🚀 Loading Stable Diffusion Model...")
    model_id = "rupeshs/LCM-runwayml-stable-diffusion-v1-5"
    
    try:
        # Create cache directory if it doesn't exist
        os.makedirs("/tmp/huggingface_cache", exist_ok=True)
        
        # Use appropriate dtype based on device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        print(f"📱 Device: {device}, dtype: {torch_dtype}")
        
        # Load the model with cache directory specified
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch_dtype,
            cache_dir="/tmp/huggingface_cache",
            local_files_only=False
        )
        
        pipe = pipe.to(device)
        
        # Skip XFormers on Windows - causes compatibility issues
        # Enable memory efficient attention if available
        # if hasattr(pipe, 'enable_xformers_memory_efficient_attention'):
        #     try:
        #         pipe.enable_xformers_memory_efficient_attention()
        #         print("✅ XFormers memory efficient attention enabled")
        #     except Exception:
        #         print("⚠️ XFormers not available, using default attention")
        
        print("✅ Using default attention (Windows compatible)")
        print(f"✅ Model Loaded successfully on {device}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        pipe = None
        return False

# Don't load model on startup - do it lazily
# model_loaded = load_model()

@app.get("/")
async def root():
    """Health check endpoint with enhanced status"""
    return {
        "status": "alive",
        "service": "PromptAgro Image Generator",
        "model_loaded": pipe is not None,
        "model_loading": model_loading,
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "model_status": "loaded" if pipe is not None else ("loading" if model_loading else "not_loaded"),
        "torch_dtype": "float16" if torch.cuda.is_available() else "float32",
        "ready_for_requests": pipe is not None
    }

@app.post("/generate/")
async def generate_image(prompt: str = Form(...)):
    """
    Generate product packaging image from input prompt.
    Returns image file directly (your original approach).
    """
    # Lazy load model on first request
    if not load_model_if_needed():
        if model_loading:
            raise HTTPException(status_code=503, detail="Model is loading, please wait...")
        else:
            raise HTTPException(status_code=503, detail="Model failed to load. Please check logs.")
    
    print(f"🖌️ Generating image for prompt: {prompt}")

    try:
        # Generate image (your original approach)
        image = pipe(prompt).images[0]

        # Save image to temp file (your original approach)
        filename = f"/tmp/{uuid.uuid4().hex}.png"
        image.save(filename)

        print(f"📦 Image saved to {filename}")

        # Return image file as response (your original approach)
        return FileResponse(filename, media_type="image/png")
    
    except Exception as e:
        print(f"❌ Image generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/generate-json/")
async def generate_image_json(
    prompt: str = Form(...),
    width: int = Form(512),
    height: int = Form(512),
    num_inference_steps: int = Form(4),  # LCM works well with few steps
    guidance_scale: float = Form(1.0)    # LCM uses low guidance
):
    """
    Generate image and return as JSON with base64 data (for frontend integration).
    """
    # Lazy load model on first request
    if not load_model_if_needed():
        if model_loading:
            raise HTTPException(status_code=503, detail="Model is loading, please wait...")
        else:
            raise HTTPException(status_code=503, detail="Model failed to load. Please check logs.")
    
    print(f"🖌️ Generating image for prompt: {prompt}")
    
    try:
        # Generate image with parameters optimized for LCM
        image = pipe(
            prompt=prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale
        ).images[0]
        
        # Convert image to base64 for JSON response
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        print("✅ Image generated successfully")
        
        return JSONResponse({
            "success": True,
            "image_data": f"data:image/png;base64,{img_str}",
            "prompt_used": prompt,
            "dimensions": {"width": width, "height": height},
            "steps": num_inference_steps
        })
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/generate-packaging/")
async def generate_packaging_specific(
    product_name: str = Form(...),
    colors: str = Form("green,yellow"),
    emotion: str = Form("trust"),
    platform: str = Form("farmers-market")
):
    """
    Generate packaging with PromptAgro-specific prompt engineering
    """
    # Lazy load model on first request
    if not load_model_if_needed():
        if model_loading:
            raise HTTPException(status_code=503, detail="Model is loading, please wait...")
        else:
            raise HTTPException(status_code=503, detail="Model failed to load. Please check logs.")
    
    # Create professional prompt for agricultural packaging
    prompt = f"""Professional agricultural product packaging design for {product_name}, 
    modern clean style, {colors.replace(',', ' and ')} color scheme, premium typography, 
    conveying {emotion}, suitable for {platform}, product photography style, 
    white background, high quality commercial design, realistic packaging mockup, 
    professional studio lighting, eco-friendly agricultural branding"""
    
    prompt = prompt.strip().replace('\n', ' ').replace('  ', ' ')
    
    print(f"🎨 Generating packaging for: {product_name}")
    print(f"📝 Using prompt: {prompt}")
    
    try:
        # Generate with packaging-optimized settings
        image = pipe(
            prompt=prompt,
            width=768,
            height=768,
            num_inference_steps=6,
            guidance_scale=1.5
        ).images[0]
        
        # Convert to base64
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return JSONResponse({
            "success": True,
            "image_data": f"data:image/png;base64,{img_str}",
            "prompt_used": prompt,
            "product_name": product_name,
            "generator": "Stable Diffusion LCM",
            "cost": "FREE",
            "processing_time": "~3-5 seconds"
        })
        
    except Exception as e:
        print(f"❌ Packaging generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
