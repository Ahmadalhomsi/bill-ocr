@echo off
title Turkish Bill OCR - Full Stack Startup
color 0A

echo.
echo ============================================
echo    Turkish Bill OCR - Full Stack Setup
echo ============================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

REM Setup Frontend
echo 📦 Setting up frontend...
if not exist "node_modules\" (
    echo Installing frontend dependencies...
    npm install --legacy-peer-deps
    if %errorlevel% neq 0 (
        echo ❌ Frontend setup failed
        pause
        exit /b 1
    )
)
echo ✅ Frontend setup complete
echo.

REM Setup Backend
echo 🔧 Setting up backend...
cd backend

if not exist "venv\" (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

if not exist "venv\Lib\site-packages\fastapi\" (
    echo Installing backend dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Backend setup failed
        pause
        exit /b 1
    )
)
echo ✅ Backend setup complete
echo.

cd ..

echo 🚀 Starting applications...
echo.
echo Frontend will be available at: http://localhost:3000
echo Backend API will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the servers
echo.

REM Start both servers
start "Backend API" cmd /k "cd backend && venv\Scripts\activate && python main.py"
timeout /t 3 >nul
start "Frontend" cmd /k "npm run dev"

echo Both servers are starting...
echo Check the opened terminal windows for status
pause
