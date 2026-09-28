@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo             VELYRA.AI — LOCAL LAUNCHER
echo              Speak English. Naturally.
echo ===================================================
echo.

REM 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10 or 3.11 from python.org.
    pause
    exit /b 1
)

REM 2. Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH.
    echo Please install Node.js (v18+) from nodejs.org.
    pause
    exit /b 1
)

REM 3. Install Python Dependencies
echo [1/4] Checking Python backend dependencies...
pip install -r backend/requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Some dependencies had warnings. Continuing...
)

REM 4. Initialize Database & Seed Curriculum
echo [2/4] Initializing SQLite database and curriculum...
python scripts/seed_database.py

REM 5. Install Frontend Dependencies
echo [3/4] Checking React frontend dependencies...
cd frontend
if not exist "node_modules\" (
    echo Installing node modules...
    call npm install
)
cd ..

REM 6. Start Backend and Frontend
echo [4/4] Starting Velyra.ai Local Servers...
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.

start "Velyra Backend (FastAPI)" cmd /k "python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"
start "Velyra Frontend (Vite)" cmd /k "cd frontend && npm run dev"

timeout /t 3 >nul
start http://localhost:5173

echo Velyra.ai is running! Press any key in the server windows to close.
