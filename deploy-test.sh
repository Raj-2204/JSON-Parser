#!/bin/bash

echo "🧪 Testing deployment setup..."

# Test backend
echo "📦 Testing backend setup..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

echo "✅ Backend dependencies installed"

# Test if backend runs
echo "🔍 Testing backend startup..."
timeout 10s python app.py &
BACKEND_PID=$!
sleep 3

if curl -s http://localhost:5001/health > /dev/null; then
    echo "✅ Backend is running successfully"
else
    echo "❌ Backend failed to start"
fi

kill $BACKEND_PID 2>/dev/null

# Test frontend
echo "📦 Testing frontend setup..."
cd ..
npm install
echo "✅ Frontend dependencies installed"

# Test frontend build
echo "🔍 Testing frontend build..."
npm run build
if [ -d "dist" ]; then
    echo "✅ Frontend build successful"
    echo "📂 Build output in dist/ directory"
else
    echo "❌ Frontend build failed"
fi

echo "🎉 Deployment test complete!"
echo ""
echo "📋 Next steps:"
echo "1. Push code to GitHub"
echo "2. Follow DEPLOYMENT.md for hosting setup"
echo "3. Update VITE_API_BASE_URL with your backend URL"