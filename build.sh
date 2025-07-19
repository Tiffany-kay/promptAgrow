#!/bin/bash
# Render.com build script for PromptAgro Backend

echo "🚀 Building PromptAgro for Render..."

# Navigate to backend directory
cd backend

# Upgrade pip to latest version
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating storage directories..."
mkdir -p storage/uploads storage/designs storage/mockups static

# Create placeholder files to ensure directories exist
touch storage/.gitkeep
touch static/.gitkeep

# Set proper permissions
chmod -R 755 storage static

echo "✅ Build completed successfully!"
echo "🌐 Starting FastAPI server..."
