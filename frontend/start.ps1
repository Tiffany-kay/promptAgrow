# PromptAgro Frontend Launcher for Windows PowerShell
Write-Host "🌾 Starting PromptAgro Frontend..." -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "index.html")) {
    Write-Host "❌ Error: index.html not found. Please run from the frontend directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "🔍 Looking for available servers..." -ForegroundColor Yellow

# Try Python first
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "🐍 Using Python server..." -ForegroundColor Cyan
        Write-Host "🌐 Open http://localhost:3000 in your browser" -ForegroundColor Green
        Write-Host ""
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
        python -m http.server 3000
        exit 0
    }
} catch {
    # Python not found, continue
}

# Try Node.js http-server
try {
    $nodeVersion = npx --version 2>$null
    if ($nodeVersion) {
        Write-Host "📦 Using Node.js http-server..." -ForegroundColor Cyan
        Write-Host "🌐 Open http://localhost:3000 in your browser" -ForegroundColor Green
        Write-Host ""
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
        npx http-server -p 3000 -c-1
        exit 0
    }
} catch {
    # Node.js not found, continue
}

# If nothing works
Write-Host "❌ No suitable server found!" -ForegroundColor Red
Write-Host ""
Write-Host "Please install one of the following:" -ForegroundColor Yellow
Write-Host "  1. Python: https://python.org" -ForegroundColor White
Write-Host "  2. Node.js: https://nodejs.org" -ForegroundColor White
Write-Host ""
Write-Host "Then run this script again." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
