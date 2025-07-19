#!/bin/bash
# PromptAgro Production Deployment Script

echo "🚀 Deploying PromptAgro to Production..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    print_warning "No .env file found. Creating from template..."
    cp backend/.env.production backend/.env
    print_warning "Please update backend/.env with your actual API keys before deploying!"
fi

# Check if config is updated
if grep -q "your-backend-domain" frontend/js/config.js; then
    print_warning "Please update frontend/js/config.js with your actual backend URL!"
fi

# Build and test
print_status "Testing backend locally..."
cd backend
python -m pytest || print_warning "No tests found - consider adding tests for production"

# Install production dependencies
print_status "Installing production dependencies..."
pip install -r requirements.txt

cd ..

# Deploy options
echo ""
echo "🚀 Choose deployment option:"
echo "1) Render.com (Recommended)"
echo "2) Heroku"
echo "3) Docker"
echo "4) Manual"

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        print_status "Render.com deployment setup..."
        print_status "1. Push your code to GitHub: git add . && git commit -m 'Deploy' && git push"
        print_status "2. Go to https://render.com/"
        print_status "3. Create 'Web Service' from your GitHub repo"
        print_status "4. Set Build Command: ./build.sh"
        print_status "5. Set Start Command: ./start.sh"
        print_status "6. Add environment variable: GEMINI_API_KEY=your_key"
        print_status "7. Deploy!"
        echo ""
        print_status "📖 Full guide: See RENDER_DEPLOY.md"
        ;;
    2)
        print_status "Deploying to Heroku..."
        print_status "Deploying to Heroku..."
        # Check if Heroku CLI is installed
        if command -v heroku &> /dev/null; then
            heroku create promptagro-app --region us
            heroku config:set DEBUG=False
            heroku config:set GEMINI_API_KEY="$(grep GEMINI_API_KEY backend/.env | cut -d '=' -f2)"
            git add .
            git commit -m "Deploy to production"
            git push heroku main
            heroku open
        else
            print_error "Heroku CLI not installed. Install from: https://devcenter.heroku.com/articles/heroku-cli"
        fi
        ;;
    2)
        print_status "Railway deployment setup..."
        print_status "1. Push your code to GitHub"
        print_status "2. Go to https://railway.app/"
        print_status "3. Connect your GitHub repo"
        print_status "4. Set environment variables in Railway dashboard"
        ;;
    3)
        print_status "Building Docker containers..."
        docker-compose build
        docker-compose up -d
        print_status "App running at http://localhost:3000"
        ;;
    4)
        print_status "Manual deployment checklist:"
        echo "1. Set up your server (VPS, AWS EC2, etc.)"
        echo "2. Copy files to server"
        echo "3. Install Python 3.11+"
        echo "4. Install dependencies: pip install -r backend/requirements.txt"
        echo "5. Set environment variables"
        echo "6. Run: uvicorn app.main:app --host 0.0.0.0 --port 8000"
        echo "7. Set up reverse proxy (nginx)"
        echo "8. Configure domain and SSL"
        ;;
esac

print_status "Deployment script complete!"
