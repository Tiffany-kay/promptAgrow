# 🚀 Deploy PromptAgro to Render.com

## Quick Deploy to Render (Recommended)

### Step 1: Prepare Your Repository
1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

### Step 2: Deploy Backend to Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `promptagro-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `./start.sh`
   - **Auto-Deploy**: `Yes`

### Step 3: Set Environment Variables
In the Render dashboard, add these environment variables:
- `GEMINI_API_KEY`: Your Google AI API key ([Get it here](https://makersuite.google.com/app/apikey))
- `DEBUG`: `False`
- `CORS_ORIGINS`: `https://your-frontend-domain.onrender.com`

### Step 4: Deploy Frontend to Render
1. Click "New" → "Static Site"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `promptagro-frontend`
   - **Build Command**: `echo "Static site ready"`
   - **Publish Directory**: `frontend`

### Step 5: Update Frontend Config
1. Once backend is deployed, copy its URL (e.g., `https://promptagro-backend.onrender.com`)
2. Update `frontend/js/config.js`:
   ```javascript
   BASE_URL: 'https://your-backend-url.onrender.com/api'
   ```
3. Redeploy frontend

## 🎯 Alternative: One Repository, Two Services

You can deploy both from the same repository:

### Backend Service:
- **Root Directory**: `/`
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Service:
- **Root Directory**: `/`
- **Build Command**: `echo "Frontend ready"`
- **Publish Directory**: `frontend`

## 🔧 Environment Variables for Render

Set these in your Render dashboard:

### Required:
- `GEMINI_API_KEY`: Your Google AI API key
- `DEBUG`: `False`
- `CORS_ORIGINS`: Your frontend domain

### Optional:
- `MAX_UPLOAD_SIZE`: `10485760`
- `CLEANUP_DAYS`: `30`

## 🌐 Custom Domain (Optional)

1. In Render dashboard → Settings → Custom Domains
2. Add your domain: `yourdomain.com`
3. Update DNS records as instructed
4. SSL certificate is automatically provided

## 📊 Monitoring

Render provides:
- Real-time logs
- Metrics and monitoring  
- Automatic health checks
- Zero-downtime deployments

## 💰 Pricing

- **Free Tier**: Perfect for testing
- **Starter**: $7/month for production
- **Standard**: $25/month for high traffic

## 🔍 Troubleshooting

### Build Fails?
- Check build logs in Render dashboard
- Ensure `requirements.txt` is in `backend/` directory
- Verify Python version compatibility

### App Won't Start?
- Check start command is correct
- Verify environment variables are set
- Check application logs

### CORS Errors?
- Add frontend domain to `CORS_ORIGINS`
- Format: `https://your-frontend.onrender.com`

## ✅ Success!

Your PromptAgro app should now be live at:
- Backend: `https://your-backend.onrender.com`
- Frontend: `https://your-frontend.onrender.com`
- API Docs: `https://your-backend.onrender.com/docs`

## 🚀 Next Steps

1. **Custom Domain**: Add your own domain
2. **Database**: Add PostgreSQL for user accounts
3. **CDN**: Use Cloudflare for faster loading
4. **Analytics**: Add Google Analytics
5. **Monitoring**: Set up error tracking

Happy farming with AI! 🌾✨
