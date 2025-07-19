@echo off
echo Starting PromptAgro Backend...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please update .env file with your API keys
)

REM Create storage directories
if not exist "storage" mkdir storage
if not exist "storage\uploads" mkdir storage\uploads
if not exist "storage\designs" mkdir storage\designs
if not exist "storage\mockups" mkdir storage\mockups

REM Create static directory and sample files
if not exist "static" mkdir static
echo Creating sample mockup for testing...
echo. > static\sample-mockup.jpg
echo. > static\sample-design.pdf

REM Start the server
echo Starting FastAPI server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
