@echo off
echo.
echo =====================================
echo   PromptAgro - AI Agri-Packaging
echo =====================================
echo.
echo Starting development server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using Python server...
    cd frontend
    echo Open http://localhost:8000 in your browser
    python -m http.server 8000
) else (
    REM Check if Node.js is available
    node --version >nul 2>&1
    if %errorlevel% == 0 (
        echo Using Node.js server...
        cd frontend
        echo Open http://localhost:3000 in your browser
        npx serve . -p 3000
    ) else (
        echo.
        echo Please install Python or Node.js to run the development server.
        echo.
        echo Python: https://python.org
        echo Node.js: https://nodejs.org
        echo.
        echo Alternatively, you can open frontend/index.html directly in your browser.
        pause
    )
)
