#!/usr/bin/env python3
"""
Simple HTTP server for bill analysis
Alternative to FastAPI - uses built-in Python HTTP server
"""

import os
import sys
import json
import cgi
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import tempfile
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_analyzer import SimpleBillAnalyzer

class BillAnalysisHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_simple_response(200, {
                "message": "GPT-4o Bill Analysis Server",
                "status": "running",
                "version": "2.0.0"
            })
        elif parsed_path.path == '/health':
            api_key_configured = bool(os.getenv("OPENAI_API_KEY"))
            self.send_simple_response(200, {
                "status": "healthy",
                "gpt4o_available": api_key_configured,
                "timestamp": datetime.now().isoformat()
            })
        else:
            self.send_simple_response(404, {"error": "Not found"})

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/process-bill':
            self.handle_bill_analysis()
        else:
            self.send_simple_response(404, {"error": "Not found"})

    def handle_bill_analysis(self):
        """Handle bill analysis request"""
        try:
            # Parse multipart form data
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                self.send_simple_response(400, {"error": "Content-Type must be multipart/form-data"})
                return

            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_simple_response(400, {"error": "No content"})
                return

            # Read the form data
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': content_type}
            )

            # Check if file was uploaded
            if 'file' not in form_data:
                self.send_simple_response(400, {"error": "No file uploaded"})
                return

            file_item = form_data['file']
            if not file_item.filename:
                self.send_simple_response(400, {"error": "No file selected"})
                return

            # Check file type
            filename = file_item.filename.lower()
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
            if not any(filename.endswith(ext) for ext in allowed_extensions):
                self.send_simple_response(400, {"error": "Unsupported file format"})
                return

            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
                temp_file.write(file_item.file.read())
                temp_path = temp_file.name

            try:
                # Analyze the bill
                analyzer = SimpleBillAnalyzer()
                result = analyzer.analyze_bill(temp_path)
                
                # Send response
                self.send_simple_response(200, {
                    "success": result.get("success", False),
                    "filename": file_item.filename,
                    "result": result
                })

            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_path)
                except:
                    pass

        except Exception as e:
            self.send_simple_response(500, {"error": f"Server error: {str(e)}"})

    def send_simple_response(self, status_code: int, data: dict):
        """Send a JSON response"""
        response_data = json.dumps(data, ensure_ascii=False, indent=2)
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(response_data.encode('utf-8'))

    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def main():
    port = int(os.environ.get('PORT', 8001))
    server_address = ('', port)
    
    print(f"🚀 Starting GPT-4o Bill Analysis Server on port {port}")
    print(f"📍 Server will be available at: http://localhost:{port}")
    print("🔑 Make sure your OpenAI API key is configured in .env file")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        httpd = HTTPServer(server_address, BillAnalysisHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()

if __name__ == "__main__":
    main()
