@echo off
echo 🚀 Setting up GPT-4o Bill Analysis (Frontend Only)
echo ==============================================

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

echo ✅ Node.js is installed

REM Install dependencies
echo.
echo 📦 Installing dependencies...
npm install

echo ✅ Dependencies installed

REM Setup environment file
echo.
echo 🔑 Setting up environment configuration...
if not exist ".env.local" (
    copy .env.local.example .env.local
    echo ✅ Created .env.local file
    echo.
    echo ⚠️  IMPORTANT: Configure your OpenAI API key
    echo 1. Edit .env.local file
    echo 2. Add your OpenAI API key:
    echo    NEXT_PUBLIC_OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    echo.
    echo 💡 Get your API key from: https://platform.openai.com/api-keys
) else (
    echo ✅ .env.local already exists
)

echo.
echo 🎉 Setup complete!
echo.
echo 🚀 To start the application:
echo    npm run dev
echo.
echo 🌐 Then open: http://localhost:3000
echo.
echo ⚠️  Security Notice:
echo    This setup exposes your API key to users.
echo    For production, consider using serverless functions or a backend proxy.
echo.
pause
