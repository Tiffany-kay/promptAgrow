#!/bin/bash
# Render.com start script for PromptAgro Backend

echo "🌾 Starting PromptAgro Backend on Render..."

# Navigate to backend directory
cd backend

# Set default port if not provided by Render
export PORT=${PORT:-8000}

# Start the FastAPI application with uvicorn
echo "🚀 Starting server on port $PORT..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2 --log-level info
