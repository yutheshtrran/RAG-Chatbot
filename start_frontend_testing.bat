@echo off
REM Frontend Testing Script for Smart PDF Upload
REM Run this batch file to start everything automatically

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  FRONTEND TESTING - SMART PDF UPLOAD                          ║
echo ║  This will start Backend and Frontend servers                 ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ❌ Error: backend directory not found
    echo Please run this script from the workspace root directory
    echo (D:\IRP_RAG_BOT\RAG-Chatbot)
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ❌ Error: frontend directory not found
    echo Please run this script from the workspace root directory
    echo (D:\IRP_RAG_BOT\RAG-Chatbot)
    pause
    exit /b 1
)

echo 📋 Checking prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found in PATH
    echo Please install Python or add it to PATH
    pause
    exit /b 1
)
echo ✅ Python found: 
python --version

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Node.js not found - will attempt npm anyway
) else (
    echo ✅ Node.js found: 
    node --version
)

echo.
echo ──────────────────────────────────────────────────────────────────
echo STARTING SERVERS...
echo ──────────────────────────────────────────────────────────────────
echo.

REM Start Backend in new window
echo 📦 Starting Backend API Server (http://127.0.0.1:5000)...
start "RAG Chatbot Backend" cmd /k "cd backend && python run.py"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start Frontend in new window
echo 🎨 Starting Frontend Dev Server (http://localhost:5173)...
start "RAG Chatbot Frontend" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo ✅ Servers starting in new windows...
echo.
echo 📖 NEXT STEPS:
echo ──────────────────────────────────────────────────────────────────
echo 1. Wait ~15 seconds for both servers to fully start
echo 2. Open your browser and go to: http://localhost:5173
echo 3. Click "Upload Patient Document" button
echo 4. Select file: backend/data/uploads/test_patient_no_id.txt
echo 5. Leave "Patient ID" field EMPTY
echo 6. Click "Upload"
echo 7. You should see: "Emily Johnson (52, Female)"
echo 8. Ask in chat: "What is the diagnosis?"
echo 9. Expect response about chronic migraines
echo.
echo ✨ That's it! You've tested the smart upload feature!
echo.
echo 📚 For detailed guide, see: FRONTEND_TESTING_GUIDE.md
echo ──────────────────────────────────────────────────────────────────
echo.

pause
