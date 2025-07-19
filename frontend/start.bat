@echo off
REM PromptAgro Frontend Launcher for Windows
echo 🌾 Starting PromptAgro Frontend...
echo.

REM Check if we're in the right directory
if not exist "index.html" (
    echo ❌ Error: index.html not found. Please run from the frontend directory.
    pause
    exit /b 1
)

REM Try different server options
echo 🔍 Looking for available servers...

REM Try Python 3 first
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo 🐍 Using Python server...
    echo 🌐 Open http://localhost:3000 in your browser
    echo.
    echo Press Ctrl+C to stop the server
    python -m http.server 3000
    goto :end
)

REM Try Node.js http-server if available
npx --version >nul 2>&1
if %errorlevel% == 0 (
    echo 📦 Using Node.js http-server...
    echo 🌐 Open http://localhost:3000 in your browser
    echo.
    echo Press Ctrl+C to stop the server
    npx http-server -p 3000 -c-1
    goto :end
)

REM If nothing works, show instructions
echo ❌ No suitable server found!
echo.
echo Please install one of the following:
echo   1. Python: https://python.org
echo   2. Node.js: https://nodejs.org
echo.
echo Then run this script again.
pause

:end
