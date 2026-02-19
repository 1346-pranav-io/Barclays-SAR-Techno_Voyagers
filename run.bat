@echo off
REM SAR Narrative Generator - Windows Startup Script

echo SAR Narrative Generator - Starting...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo No .env file found. Creating from template...
    copy .env.example .env
    echo Please edit .env and add your Anthropic API key
    echo.
)

REM Initialize database
echo Initializing database...
python -c "from database import init_db; init_db()"

echo.
echo Setup complete!
echo.
echo Starting Streamlit application...
echo.
echo The app will open in your browser at http://localhost:8501
echo.

REM Run Streamlit
streamlit run app.py

pause
