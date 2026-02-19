#!/bin/bash

# SAR Narrative Generator - Startup Script

echo "🔍 SAR Narrative Generator - Starting..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your Anthropic API key"
    echo ""
fi

# Initialize database
echo "Initializing database..."
python -c "from database import init_db; init_db()"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Streamlit application..."
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo ""

# Run Streamlit
streamlit run app.py
