#!/bin/bash

echo "🚀 Setting up GPT-4o Bill Analysis (Secure)"
echo "========================================"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

echo "✅ Node.js is installed"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

echo "✅ Dependencies installed"

# Setup environment file
echo ""
echo "🔑 Setting up environment configuration..."
if [ ! -f ".env.local" ]; then
    cp .env.local.example .env.local
    echo "✅ Created .env.local file"
    echo ""
    echo "⚠️  IMPORTANT: Configure your OpenAI API key"
    echo "1. Edit .env.local file"
    echo "2. Add your OpenAI API key:"
    echo "   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    echo ""
    echo "💡 Get your API key from: https://platform.openai.com/api-keys"
else
    echo "✅ .env.local already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "   npm run dev"
echo ""
echo "🌐 Then open: http://localhost:3000"
echo ""
echo "✅ Security Notice:"
echo "   Your API key is now secure and only used server-side."
echo "   Safe for production deployment!"
