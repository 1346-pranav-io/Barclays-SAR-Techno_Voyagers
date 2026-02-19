# 🚀 Quick Start Guide

## Get Running in 5 Minutes!

### Step 1: Prerequisites
- Python 3.9+ installed
- 500MB free disk space
- Internet connection

### Step 2: Get Anthropic API Key
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Go to "API Keys"
4. Create a new key
5. Copy it (you'll need it in Step 4)

### Step 3: Extract Files
Extract all files from this package to a folder, e.g., `sar-generator`

### Step 4: Easy Launch

**On Windows:**
1. Double-click `run.bat`
2. Enter your API key when the app opens

**On Mac/Linux:**
1. Open terminal in the folder
2. Run: `bash run.sh`
3. Enter your API key when the app opens

**Manual Method (All platforms):**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Step 5: Try the Demo
1. App opens at http://localhost:8501
2. Enter API key in sidebar
3. Click "Load Example Case"
4. Click "🚀 Generate SAR Narrative"
5. Wait 30-60 seconds
6. Explore the generated narrative and audit trail!

---

## 📁 Files Included

- `app.py` - Main Streamlit application
- `sar_generator.py` - Core SAR generation logic
- `database.py` - Database models
- `sample_data.py` - Sample data generator
- `config.py` - Configuration
- `requirements.txt` - Python dependencies
- `README.md` - Full documentation
- `DEMO_GUIDE.md` - Complete demo walkthrough
- `ARCHITECTURE.md` - Technical architecture
- `run.sh` - Linux/Mac startup script
- `run.bat` - Windows startup script
- `.env.example` - Environment template

---

## 🆘 Troubleshooting

**"Python not found"**
→ Install Python 3.9+ from python.org

**"API key error"**
→ Check your Anthropic API key is correct and has credits

**"ModuleNotFoundError"**
→ Run: `pip install -r requirements.txt`

**"Port already in use"**
→ Run: `streamlit run app.py --server.port 8502`

---

## 📖 Next Steps

1. Read `DEMO_GUIDE.md` for complete walkthrough
2. Read `README.md` for full documentation
3. Read `ARCHITECTURE.md` for technical details
4. Start generating SARs!

---

**Questions?** Check the README.md file for detailed documentation.

**Ready for production?** See ARCHITECTURE.md for AWS migration guide.
