#!/bin/bash

echo "🚀 Starting Image Background Remover API..."
echo "📦 Activating virtual environment..."

# Activate virtual environment
source venv/bin/activate

echo "🔧 Installing dependencies (if needed)..."
pip install Flask Flask-CORS Pillow rembg numpy requests > /dev/null 2>&1

echo "🎯 Starting Flask server..."
echo "📡 The API will be available at: http://localhost:5000"
echo "🌐 Open frontend.html in your browser to test the API"
echo ""
echo "⏳ Note: First run may take a few minutes as rembg downloads the AI model (~176MB)"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python app.py