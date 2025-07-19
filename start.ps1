# PromptAgro Development Server Launcher (PowerShell)
Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "  PromptAgro - AI Agri-Packaging" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Starting development server..." -ForegroundColor Yellow
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Using Python server..." -ForegroundColor Cyan
        Set-Location frontend
        Write-Host "Open http://localhost:8000 in your browser" -ForegroundColor Green
        Write-Host ""
        python -m http.server 8000
    }
} catch {
    # Check if Node.js is available
    try {
        $nodeVersion = node --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Using Node.js server..." -ForegroundColor Cyan
            Set-Location frontend
            Write-Host "Open http://localhost:3000 in your browser" -ForegroundColor Green
            Write-Host ""
            npx serve . -p 3000
        }
    } catch {
        Write-Host ""
        Write-Host "Please install Python or Node.js to run the development server." -ForegroundColor Red
        Write-Host ""
        Write-Host "Python: https://python.org" -ForegroundColor Blue
        Write-Host "Node.js: https://nodejs.org" -ForegroundColor Blue
        Write-Host ""
        Write-Host "Alternatively, you can open frontend/index.html directly in your browser." -ForegroundColor Yellow
        Read-Host "Press Enter to continue"
    }
}
