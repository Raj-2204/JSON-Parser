# 🚀 Deployment Guide

This guide covers multiple deployment options for your JSON Parser application.

## 📋 Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Hosting Account** - Choose from the options below

---

## 🎯 **Option 1: Render.com (Recommended)**

### **Why Render.com?**
- ✅ Free tier available
- ✅ Easy GitHub integration
- ✅ Automatic deployments
- ✅ Supports both React and Flask
- ✅ Built-in SSL certificates

### **Steps:**

#### **1. Push to GitHub**
```bash
cd /path/to/json-parser-frontend
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/json-parser-frontend.git
git push -u origin main
```

#### **2. Deploy Backend**
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `json-parser-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
5. Add Environment Variables:
   - `FLASK_ENV` = `production`
6. Click "Create Web Service"

#### **3. Deploy Frontend**
1. Click "New +" → "Static Site"
2. Connect same GitHub repository
3. Configure:
   - **Name**: `json-parser-frontend`
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add Environment Variable:
   - `VITE_API_BASE_URL` = `https://your-backend-url.onrender.com`
   - (Copy the backend URL from step 2)
5. Click "Create Static Site"

---

## 🎯 **Option 2: Vercel + Railway**

### **Deploy Backend on Railway**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Configure:
   - **Root Directory**: `backend`
   - Add environment variables as needed
6. Deploy!

### **Deploy Frontend on Vercel**
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Import your repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `/`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add environment variable:
   - `VITE_API_BASE_URL` = your Railway backend URL
6. Deploy!

---

## 🎯 **Option 3: Netlify + Heroku**

### **Deploy Backend on Heroku**
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app:
   ```bash
   cd backend
   heroku create your-app-name-backend
   ```
4. Add Procfile:
   ```bash
   echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT app:app" > Procfile
   ```
5. Deploy:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### **Deploy Frontend on Netlify**
1. Build locally:
   ```bash
   npm run build
   ```
2. Go to [netlify.com](https://netlify.com)
3. Drag and drop the `dist` folder
4. Or connect to GitHub for automatic deployments

---

## 🔧 **Environment Variables**

### **Backend (.env)**
```
FLASK_ENV=production
PORT=5001
```

### **Frontend (.env.production)**
```
VITE_API_BASE_URL=https://your-backend-url.onrender.com
```

---

## 🧪 **Testing Deployment**

1. **Health Check**: Visit `https://your-backend-url/health`
2. **Frontend**: Visit your frontend URL
3. **Full Test**: Try parsing JSON in the deployed app

---

## 🐛 **Troubleshooting**

### **Common Issues:**

#### **CORS Errors**
- Ensure Flask-CORS is properly configured
- Check if frontend URL is allowed in CORS settings

#### **Import Errors**
- Verify all Python files are in the backend directory
- Check requirements.txt includes all dependencies

#### **Build Failures**
- Check Node.js version compatibility
- Verify all npm packages are in package.json

#### **API Connection Issues**
- Confirm `VITE_API_BASE_URL` points to correct backend
- Check network/firewall settings

---

## 📱 **Custom Domain (Optional)**

### **Render.com**
1. Go to service settings
2. Add custom domain
3. Configure DNS records as shown

### **Vercel**
1. Go to project settings
2. Domains → Add domain
3. Configure DNS records

---

## 🔄 **Auto-Deployment**

All platforms support automatic deployment on Git push:
- **Render**: Automatically rebuilds on push to main branch
- **Vercel**: Automatic deployments with preview URLs
- **Netlify**: Continuous deployment from Git

Your JSON Parser app will be live and accessible worldwide! 🌍