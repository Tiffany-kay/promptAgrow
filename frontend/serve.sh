#!/bin/bash
# Simple launcher for PromptAgro frontend

echo "🌾 Starting PromptAgro Frontend..."
echo ""

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found. Please run from the frontend directory."
    exit 1
fi

# Try different server options
if command -v python3 &> /dev/null; then
    echo "🐍 Using Python 3 server..."
    echo "🌐 Open http://localhost:8000 in your browser"
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    echo "🐍 Using Python server..."
    echo "🌐 Open http://localhost:8000 in your browser"
    python -m http.server 8000
elif command -v node &> /dev/null; then
    echo "🟢 Using Node.js server..."
    echo "🌐 Open http://localhost:3000 in your browser"
    npx serve . -p 3000
else
    echo "❌ No server found. Please install Python or Node.js"
    echo "📂 You can also open index.html directly in your browser"
fi
