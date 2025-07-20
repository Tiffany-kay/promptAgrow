# Dockerfile for PromptAgro
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Pre-create cache directory (optional)
RUN mkdir -p /app/cache

# Set up cache directories and environment variables
RUN mkdir -p /tmp/huggingface_cache
ENV HF_HOME=/tmp/huggingface_cache
ENV TRANSFORMERS_CACHE=/tmp/huggingface_cache
ENV HF_HUB_CACHE=/tmp/huggingface_cache

# Expose port
EXPOSE 7860

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
