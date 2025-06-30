#!/usr/bin/env python3
"""
Simple GPT-4o Bill Analyzer
A command-line tool to analyze bill images using GPT-4o Vision API
"""

import os
import sys
import json
import base64
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from PIL import Image
import io

# Add the current directory to the path to import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings

try:
    from openai import OpenAI
except ImportError:
    print("❌ OpenAI package not installed. Run: pip install openai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install it for .env file support: pip install python-dotenv")

class SimpleBillAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY
        if not self.api_key:
            print("❌ OpenAI API key not found!")
            print("Set OPENAI_API_KEY environment variable or add it to .env file")
            sys.exit(1)
        
        self.client = OpenAI(api_key=self.api_key)
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        return """
You are an expert at analyzing bill/receipt images and extracting structured data. 
Analyze the uploaded bill image and extract the following information in JSON format:

{
  "dates": ["list of dates found in the bill"],
  "items": [
    {
      "name": "item name",
      "quantity": "quantity with unit (e.g., '2 kg', '1 adet')",
      "unit_price": "price per unit if available",
      "total_price": "total price for this item",
      "line_text": "original text line where this item was found"
    }
  ],
  "amounts": [
    {
      "value": "numerical value",
      "currency": "currency symbol or code",
      "description": "what this amount represents (e.g., 'subtotal', 'tax', 'total')",
      "original_text": "original text as it appears in the bill"
    }
  ],
  "totals": {
    "subtotal": "subtotal amount if available",
    "tax": "tax amount if available", 
    "total": "final total amount",
    "currency": "currency used"
  },
  "merchant_info": {
    "name": "merchant/store name if visible",
    "address": "address if visible",
    "phone": "phone number if visible"
  },
  "bill_metadata": {
    "bill_number": "receipt/bill number if available",
    "cashier": "cashier name/ID if available",
    "payment_method": "payment method if specified"
  }
}

IMPORTANT INSTRUCTIONS:
1. Extract ALL visible text accurately
2. For Turkish bills, recognize Turkish characters properly (ç, ğ, ı, ö, ş, ü)
3. Parse dates in various formats (DD/MM/YYYY, DD.MM.YYYY, etc.)
4. Identify currency symbols (₺ for Turkish Lira, $ for Dollar, € for Euro)
5. Extract quantities and units (kg, gr, lt, adet, paket, etc.)
6. Calculate totals when possible
7. If information is not available, use null or empty string
8. Be precise with numerical values
9. Preserve original text formatting when possible

Return ONLY the JSON response, no additional text or formatting.
"""

    def encode_image_to_base64(self, image_path: str) -> str:
        """Convert image file to base64 string"""
        try:
            with Image.open(image_path) as image:
                # Convert to RGB if needed
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Resize if too large
                if image.width > settings.IMAGE_MAX_WIDTH or image.height > settings.IMAGE_MAX_HEIGHT:
                    image.thumbnail((settings.IMAGE_MAX_WIDTH, settings.IMAGE_MAX_HEIGHT), Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG', quality=settings.IMAGE_QUALITY)
                buffer.seek(0)
                return base64.b64encode(buffer.read()).decode('utf-8')
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")

    def analyze_bill(self, image_path: str) -> Dict[str, Any]:
        """Analyze a bill image using GPT-4o Vision API"""
        print(f"📸 Processing image: {image_path}")
        
        # Validate file
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        file_ext = Path(image_path).suffix.lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        # Check file size
        file_size = os.path.getsize(image_path)
        if file_size > settings.MAX_FILE_SIZE:
            raise ValueError(f"File too large: {file_size / 1024 / 1024:.1f}MB (max: {settings.MAX_FILE_SIZE / 1024 / 1024}MB)")
        
        try:
            # Encode image
            print("🔄 Encoding image...")
            base64_image = self.encode_image_to_base64(image_path)
            
            # Prepare GPT-4o request
            print("🤖 Sending to GPT-4o...")
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please analyze this bill/receipt image and extract the structured data as requested."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ]
            
            # Call GPT-4o API
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=settings.OPENAI_TEMPERATURE
            )
            
            # Parse response
            response_text = response.choices[0].message.content.strip()
            
            # Clean up response (remove markdown formatting if present)
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            # Parse JSON
            try:
                extracted_data = json.loads(response_text)
                
                # Add metadata
                result = {
                    "success": True,
                    "filename": os.path.basename(image_path),
                    "timestamp": datetime.now().isoformat(),
                    "model": settings.OPENAI_MODEL,
                    "tokens_used": response.usage.total_tokens if response.usage else None,
                    "extracted_data": extracted_data,
                    "raw_response": response_text
                }
                
                print("✅ Analysis completed successfully!")
                return result
                
            except json.JSONDecodeError as e:
                print(f"⚠️  Failed to parse JSON response: {e}")
                return {
                    "success": False,
                    "error": "Failed to parse JSON response",
                    "raw_response": response_text,
                    "filename": os.path.basename(image_path),
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            return {
                "success": False,
                "error": str(e),
                "filename": os.path.basename(image_path),
                "timestamp": datetime.now().isoformat()
            }

def main():
    parser = argparse.ArgumentParser(description="Analyze bill images using GPT-4o Vision API")
    parser.add_argument("image_path", help="Path to the bill image file")
    parser.add_argument("--output", "-o", help="Output file path (JSON format)")
    parser.add_argument("--pretty", "-p", action="store_true", help="Pretty print JSON output")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = SimpleBillAnalyzer()
    
    # Analyze the bill
    result = analyzer.analyze_bill(args.image_path)
    
    # Format output
    if args.pretty:
        json_output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        json_output = json.dumps(result, ensure_ascii=False)
    
    # Output results
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"📄 Results saved to: {args.output}")
    else:
        print("\n📊 Analysis Results:")
        print("=" * 50)
        print(json_output)
    
    # Show summary if verbose
    if args.verbose and result.get("success"):
        data = result.get("extracted_data", {})
        print(f"\n📋 Summary:")
        print(f"- Items found: {len(data.get('items', []))}")
        print(f"- Dates found: {len(data.get('dates', []))}")
        print(f"- Amounts found: {len(data.get('amounts', []))}")
        if data.get('totals', {}).get('total'):
            print(f"- Total amount: {data['totals']['total']} {data['totals'].get('currency', '')}")
        if data.get('merchant_info', {}).get('name'):
            print(f"- Merchant: {data['merchant_info']['name']}")

if __name__ == "__main__":
    main()
