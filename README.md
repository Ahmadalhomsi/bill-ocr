# GPT-4o Bill Analysis

A modern web application for extracting structured data from bills and receipts using GPT-4o Vision API.

## Features

- 🖼️ **Drag & Drop Upload**: Easy image upload with preview
- 🤖 **GPT-4o Vision**: Advanced AI-powered text extraction and analysis
- 🇹🇷 **Multi-language Support**: Works with Turkish, English, and other languages
- 📊 **Smart Data Extraction**: Automatically extracts dates, items, amounts, and metadata
- 🏪 **Merchant Information**: Extracts store names, addresses, and contact details
- � **Bill Metadata**: Captures receipt numbers, cashier info, and payment methods
- 💰 **Automatic Calculations**: Calculates totals and validates amounts
- 🎨 **Modern UI**: Beautiful, responsive design with dark mode support
- ⚡ **Fast Processing**: Direct API integration with OpenAI

## Architecture

- **Frontend**: Next.js 15 with TypeScript and Tailwind CSS
- **AI Engine**: OpenAI GPT-4o Vision API (direct integration)
- **Deployment**: Can be deployed to Vercel, Netlify, or any static hosting

## Quick Setup (2 minutes)

### Prerequisites

- Node.js 18+
- OpenAI API Key (get from [OpenAI Platform](https://platform.openai.com/api-keys))

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure API key:**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local and add your OpenAI API key:
   # NEXT_PUBLIC_OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. **Start the application:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   ```
   http://localhost:3000
   ```

⚠️ **Important**: This approach exposes your API key to users. For production, consider using serverless functions or a backend proxy.

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key:
   # OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

5. **Run the FastAPI server:**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8001`

#### Frontend Setup

1. **Install dependencies (from root directory):**
   ```bash
   npm install --legacy-peer-deps
   ```

2. **Run the development server:**
   ```bash
   npm run dev
   ```
   
   The application will be available at `http://localhost:3000`

## Usage

1. Open the application in your browser (`http://localhost:3000`)
2. Drag and drop a bill image or click to browse
3. Click "Analyze with GPT-4o" to extract data
4. View the extracted information:
   - Merchant information (name, address, phone)
   - Bill metadata (receipt number, cashier, payment method)
   - Items with quantities and prices
   - Dates and amounts found
   - Total calculated amount
   - Raw GPT-4o analysis

## API Endpoints

### `POST /process-bill`
Process a bill image using GPT-4o Vision API and extract structured data.

**Request:**
- `file`: Image file (multipart/form-data)

**Response:**
```json
{
  "success": true,
  "filename": "bill.jpg",
  "result": {
    "raw_text": {
      "gpt4o_response": "...",
      "combined": "..."
    },
    "extracted_data": {
      "dates": ["24.06.25"],
      "amounts": [...],
      "items": [...],
      "total_calculated": 1970.0,
      "item_count": 10,
      "merchant_info": {
        "name": "Store Name",
        "address": "Store Address",
        "phone": "Phone Number"
      },
      "bill_metadata": {
        "bill_number": "Receipt #123",
        "cashier": "Cashier Name",
        "payment_method": "Cash/Card"
      }
    },
    "processing_info": {
      "timestamp": "2025-06-30T...",
      "method": "gpt-4o-vision",
      "model": "gpt-4o",
      "tokens_used": 1234
    }
  }
}
```

### `POST /analyze-bill`
Get detailed GPT-4o analysis with raw response data.

### `GET /health`
Check API health and OpenAI API key configuration.

## Supported Formats

- **Image Types**: JPEG, PNG, BMP, TIFF
- **Max File Size**: 10MB
- **Languages**: Turkish, English, and many others (GPT-4o supports multiple languages)

## GPT-4o Analysis Features

The system uses GPT-4o Vision API to provide:

1. **Accurate Text Recognition**: Superior to traditional OCR, especially for handwritten text
2. **Contextual Understanding**: Understands the structure and meaning of bills
3. **Multi-language Support**: Works with various languages and scripts
4. **Structured Data Extraction**: Extracts specific fields like merchant info, items, prices
5. **Intelligent Parsing**: Identifies dates, currencies, quantities with context
6. **Error Handling**: Robust error handling and fallback responses

## Development

### Customizing GPT-4o Prompts
Edit the `system_prompt` in `backend/main.py` to modify how GPT-4o analyzes bills:

```python
self.system_prompt = """
You are an expert at analyzing bill/receipt images...
# Customize the prompt here
"""
```

### Adding New Features
- Modify the JSON schema in the system prompt
- Update the frontend interfaces to handle new data fields
- Add new UI components for additional information

## Troubleshooting

### Common Issues

1. **OpenAI API Key not configured:**
   - Create a `.env` file in the `backend` directory
   - Add your OpenAI API key: `OPENAI_API_KEY=sk-proj-...`

2. **API Rate Limits:**
   - Check your OpenAI usage dashboard
   - Consider implementing rate limiting in the application

3. **CORS errors:**
   - Ensure backend is running on port 8001
   - Check CORS settings in `backend/main.py`

4. **Image processing issues:**
   - Ensure images are in supported formats
   - Check file size limits (10MB max)
   - Verify image quality and readability
5. **Installation issues:**
   - Use `--legacy-peer-deps` for npm install
   - Ensure Python 3.8+ is installed
   - Check virtual environment activation
   - Verify OpenAI API key is valid and has sufficient credits

6. **JSON parsing errors:**
   - GPT-4o sometimes returns non-JSON responses
   - The system handles this gracefully and shows raw response
   - Try with clearer, higher-quality images

## Cost Considerations

- GPT-4o Vision API charges per token used
- Typical bill analysis uses 500-2000 tokens
- Monitor usage in your OpenAI dashboard
- Consider implementing caching for repeated analyses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Changelog

### v2.0.0 - GPT-4o Integration
- Replaced OCR engines with GPT-4o Vision API
- Added merchant information extraction
- Added bill metadata extraction
- Improved accuracy for handwritten and printed text
- Added multi-language support
- Enhanced UI with new data fields

### v1.0.0 - Initial Release
- Basic OCR using Tesseract and EasyOCR
- Turkish language optimization
- Bill data extraction
- Modern web interface

## Acknowledgments

- Tesseract OCR project
- EasyOCR project
- FastAPI framework
- Next.js framework
