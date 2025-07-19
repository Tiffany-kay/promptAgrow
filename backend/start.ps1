# PromptAgro Backend PowerShell Start Script

Write-Host "Starting PromptAgro Backend..." -ForegroundColor Green

# Check if Python is installed
try {
    python --version | Out-Null
} catch {
    Write-Host "Python is not installed or not in PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "Please update .env file with your API keys" -ForegroundColor Cyan
}

# Create storage directories
$directories = @("storage", "storage\uploads", "storage\designs", "storage\mockups", "static")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Green
    }
}

# Create sample files for testing
Write-Host "Creating sample files for testing..." -ForegroundColor Yellow
"" | Out-File "static\sample-mockup.jpg" -Encoding ascii
"" | Out-File "static\sample-design.pdf" -Encoding ascii

# Start the server
Write-Host "Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "API documentation available at http://localhost:8000/docs" -ForegroundColor Cyan
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
