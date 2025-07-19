@echo off
echo ⚡ Quick Fix: Installing PromptAgro Backend Dependencies...

REM Navigate to backend directory
cd /d "c:\Users\HP ELITEBOOK\PROMPT-AGRO\backend"

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install core dependencies one by one to avoid conflicts
echo Installing FastAPI...
pip install fastapi==0.104.1

echo Installing Uvicorn...
pip install uvicorn==0.24.0

echo Installing Pydantic...
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0

echo Installing other dependencies...
pip install python-multipart==0.0.6
pip install python-dotenv==1.0.0
pip install aiohttp==3.9.1
pip install aiofiles==23.2.1
pip install jinja2==3.1.2
pip install pillow==10.1.0

REM Try reportlab - skip if it fails
echo Installing ReportLab (may skip if issues)...
pip install reportlab==4.0.7 || echo "ReportLab skipped - will use basic PDF generation"

echo ✅ Installation complete!
echo 🚀 Starting server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
