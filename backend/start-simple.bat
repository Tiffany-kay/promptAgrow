@echo off
echo 🚀 Starting PromptAgro Backend (Simplified)...

echo Installing minimal dependencies...
pip install fastapi==0.104.1 uvicorn==0.24.0 python-multipart==0.0.6 pydantic==2.5.0 python-dotenv==1.0.0 aiofiles==23.2.1

echo Creating directories...
if not exist "storage" mkdir storage
if not exist "storage\uploads" mkdir storage\uploads
if not exist "storage\designs" mkdir storage\designs
if not exist "static" mkdir static

echo Creating sample files...
echo Sample mockup > static\sample-mockup.jpg
echo Sample design report > static\sample-design.txt

echo ✅ Starting server on http://localhost:8000
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
