#!/usr/bin/env node

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🧪 Turkish Bill OCR - System Test');
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
    console.log('   Run: cd backend && python -m venv venv && venv\\Scripts\\activate && pip install -r requirements.txt');
    process.exit(1);
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
    const port8000Available = await testPort(8000);
    
    if (!port3000Available) {
        console.log('⚠️  Port 3000 is in use (frontend)');
    } else {
        console.log('✅ Port 3000 is available (frontend)');
    }
    
    if (!port8000Available) {
        console.log('⚠️  Port 8000 is in use (backend)');
    } else {
        console.log('✅ Port 8000 is available (backend)');
    }
    
    console.log('\n📋 Test Summary:');
    console.log('- Frontend dependencies: ✅ Installed');
    console.log('- Backend virtual environment: ✅ Created');
    console.log(`- Frontend port (3000): ${port3000Available ? '✅ Available' : '⚠️  In use'}`);
    console.log(`- Backend port (8000): ${port8000Available ? '✅ Available' : '⚠️  In use'}`);
    
    console.log('\n🚀 Ready to start!');
    console.log('   Run: start.bat (Windows) or use the individual startup commands');
    console.log('   Frontend: npm run dev');
    console.log('   Backend: cd backend && venv\\Scripts\\activate && python main.py');
}

runTests().catch(console.error);
