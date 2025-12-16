@echo off
REM RAG Chatbot Quick Start Script for Windows
REM This script sets up and runs the entire project

echo.
echo ==========================================
echo   RAG Chatbot - Quick Start
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✓ Python and Node.js are installed
echo.

REM Backend Setup
echo.
echo ==========================================
echo   STEP 1: Backend Setup
echo ==========================================
echo.

cd backend

echo Installing Python dependencies...
pip install -r app/requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed
echo.

echo Initializing backend...
python init.py
if errorlevel 1 (
    echo WARNING: Initialization had issues, continuing anyway...
)

echo ✓ Backend initialized
echo.

REM Frontend Setup
echo.
echo ==========================================
echo   STEP 2: Frontend Setup
echo ==========================================
echo.

cd ..\frontend

echo Installing Node.js dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node packages
    pause
    exit /b 1
)

echo ✓ Node dependencies installed
echo.

REM Create sample data
echo.
echo ==========================================
echo   STEP 3: Creating Sample Data
echo ==========================================
echo.

cd ..\

echo Creating sample patient data...
python create_sample_data.py
if errorlevel 1 (
    echo WARNING: Failed to create sample data, continuing anyway...
)

echo ✓ Sample data created (optional)
echo.

REM Summary
echo.
echo ==========================================
echo   Setup Complete!
echo ==========================================
echo.
echo To start the application:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   python run.py
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open your browser to: http://127.0.0.1:5173
echo.
echo API Endpoint: http://127.0.0.1:5000/api
echo.
echo For detailed instructions, see SETUP_GUIDE.md and README.md
echo.

pause
