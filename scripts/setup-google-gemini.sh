#!/bin/bash
# Setup script for migrating to Google Gemini API

set -e

echo "🚀 Context-Coder: Migrando para Google Gemini API (Direto)"
echo "============================================================"
echo ""

# Check if in venv
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not active!"
    echo "Please run: source .venv/bin/activate"
    exit 1
fi

echo "✅ Virtual environment active: $VIRTUAL_ENV"
echo ""

# Navigate to backend
cd "$(dirname "$0")/../backend"

echo "📦 Installing google-generativeai SDK..."
poetry add google-generativeai

echo ""
echo "✅ Dependencies installed successfully!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Get your FREE Google AI API key:"
echo "   👉 https://aistudio.google.com/apikey"
echo ""
echo "2. Add it to backend/.env:"
echo "   GOOGLE_API_KEY=your-key-here"
echo "   GOOGLE_MODEL=gemini-2.0-flash-exp"
echo ""
echo "3. Run the backend:"
echo "   cd backend && poetry run uvicorn main:app --reload"
echo ""
echo "4. Test the health endpoint:"
echo "   curl http://localhost:8000/health"
echo ""
echo "✨ Google Gemini will be used as PRIMARY provider"
echo "🔄 OpenRouter will be FALLBACK (if Google fails)"
echo ""
