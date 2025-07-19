@echo off
REM PromptAgro Production Deployment Script for Windows

echo 🚀 Deploying PromptAgro to Production...

REM Check if .env exists
if not exist "backend\.env" (
    echo ⚠️  No .env file found. Creating from template...
    copy "backend\.env.production" "backend\.env"
    echo ⚠️  Please update backend\.env with your actual API keys before deploying!
    pause
)

REM Install dependencies
echo ✅ Installing production dependencies...
cd backend
pip install -r requirements.txt
cd ..

echo.
echo 🚀 Choose deployment option:
echo 1) Render.com (Recommended)
echo 2) Heroku
echo 3) Docker
echo 4) Manual
echo.

set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    echo ✅ Render.com deployment setup...
    echo 1. Push your code to GitHub: git add . && git commit -m "Deploy" && git push
    echo 2. Go to https://render.com/
    echo 3. Create "Web Service" from your GitHub repo
    echo 4. Set Build Command: ./build.sh
    echo 5. Set Start Command: ./start.sh  
    echo 6. Add environment variable: GEMINI_API_KEY=your_key
    echo 7. Deploy!
    echo.
    echo 📖 Full guide: See RENDER_DEPLOY.md
) else if "%choice%"=="2" (
    echo ✅ Deploying to Heroku...
    echo ✅ Deploying to Heroku...
    where heroku >nul 2>&1
    if %errorlevel% equ 0 (
        heroku create promptagro-app --region us
        heroku config:set DEBUG=False
        for /f "tokens=2 delims==" %%a in ('findstr GEMINI_API_KEY backend\.env') do heroku config:set GEMINI_API_KEY=%%a
        git add .
        git commit -m "Deploy to production"
        git push heroku main
        heroku open
    ) else (
        echo ❌ Heroku CLI not installed. Install from: https://devcenter.heroku.com/articles/heroku-cli
    )
) else if "%choice%"=="2" (
    echo ✅ Railway deployment setup...
    echo 1. Push your code to GitHub
    echo 2. Go to https://railway.app/
    echo 3. Connect your GitHub repo
    echo 4. Set environment variables in Railway dashboard
) else if "%choice%"=="3" (
    echo ✅ Building Docker containers...
    docker-compose build
    docker-compose up -d
    echo ✅ App running at http://localhost:3000
) else if "%choice%"=="4" (
    echo ✅ Manual deployment checklist:
    echo 1. Set up your server (VPS, AWS EC2, etc.)
    echo 2. Copy files to server
    echo 3. Install Python 3.11+
    echo 4. Install dependencies: pip install -r backend/requirements.txt
    echo 5. Set environment variables
    echo 6. Run: uvicorn app.main:app --host 0.0.0.0 --port 8000
    echo 7. Set up reverse proxy (nginx)
    echo 8. Configure domain and SSL
)

echo.
echo ✅ Deployment script complete!
pause
