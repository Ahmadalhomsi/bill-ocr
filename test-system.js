#!/usr/bin/env node

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const https = require('https');

console.log('🧪 GPT-4o Bill OCR - System Test');
console.log('=' .repeat(50));

// Check if Node.js dependencies are installed
if (!fs.existsSync('node_modules')) {
    console.log('❌ Frontend dependencies not installed');
    console.log('   Run: npm install --legacy-peer-deps');
    process.exit(1);
}

// Check if backend dependencies are installed
if (!fs.existsSync('backend/venv')) {
    console.log('❌ Backend virtual environment not found');
    console.log('   Run setup script or manually:');
    console.log('   cd backend && python -m venv venv && venv\\Scripts\\activate && pip install -r requirements.txt');
    process.exit(1);
}

// Check if .env file exists
if (!fs.existsSync('backend/.env')) {
    console.log('⚠️  OpenAI API key not configured');
    console.log('   Create backend/.env file with your OpenAI API key');
    console.log('   Example: OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');
}

console.log('✅ Dependencies check passed');

// Test if ports are available
const net = require('net');

function testPort(port) {
    return new Promise((resolve) => {
        const server = net.createServer();
        server.listen(port, () => {
            server.once('close', () => resolve(true));
            server.close();
        });
        server.on('error', () => resolve(false));
    });
}

async function runTests() {
    console.log('\n🔍 Checking port availability...');
    
    const port3000Available = await testPort(3000);
    const port8001Available = await testPort(8001);
    
    if (!port3000Available) {
        console.log('⚠️  Port 3000 is in use (frontend)');
    } else {
        console.log('✅ Port 3000 is available (frontend)');
    }
    
    if (!port8001Available) {
        console.log('⚠️  Port 8001 is in use (backend)');
    } else {
        console.log('✅ Port 8001 is available (backend)');
    }
    
    console.log('\n📋 Test Summary:');
    console.log('- Frontend dependencies: ✅ Installed');
    console.log('- Backend virtual environment: ✅ Created');
    console.log(`- Frontend port (3000): ${port3000Available ? '✅ Available' : '⚠️  In use'}`);
    console.log(`- Backend port (8001): ${port8001Available ? '✅ Available' : '⚠️  In use'}`);
    
    console.log('\n🚀 To start the system:');
    console.log('1. Backend: cd backend && python main.py');
    console.log('2. Frontend: npm run dev');
    console.log('3. Open: http://localhost:3000');
    console.log('\n💡 Make sure to configure your OpenAI API key in backend/.env');
    console.log('   Get your API key from: https://platform.openai.com/api-keys');
}

runTests().catch(console.error);
