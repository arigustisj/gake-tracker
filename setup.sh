#!/bin/bash

echo "🚀 Gake Tracker - Quick Setup"
echo "=============================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "✅ .env file already exists"
else
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your credentials:"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - TELEGRAM_CHAT_ID"
    echo ""
fi

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3 found: $(python3 --version)"
else
    echo "❌ Python3 not found. Please install Python 3.11+"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Telegram credentials"
echo "2. Run: python tracker.py"
echo ""
echo "For deployment to cloud:"
echo "- Railway: https://railway.app"
echo "- Render: https://render.com"
echo "- Fly.io: https://fly.io"
echo ""
echo "Read README.md for detailed instructions"
