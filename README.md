# Turkish Bill OCR

A modern web application for extracting data from handwritten Turkish bills using advanced OCR technology.

## Features

- 🖼️ **Drag & Drop Upload**: Easy image upload with preview
- 🔍 **Advanced OCR**: Uses both Tesseract and EasyOCR for better accuracy
- 🇹🇷 **Turkish Language Support**: Optimized for Turkish text recognition
- 📊 **Smart Data Extraction**: Automatically extracts dates, amounts, and items
- 💰 **Total Calculation**: Automatically calculates total amounts
- 🎨 **Modern UI**: Beautiful, responsive design with dark mode support
- ⚡ **Fast Processing**: Efficient image preprocessing and OCR processing

## Architecture

- **Frontend**: Next.js 15 with TypeScript and Tailwind CSS
- **Backend**: FastAPI with Python
- **OCR Engines**: Tesseract and EasyOCR
- **Image Processing**: OpenCV and PIL

## Setup Instructions

### Prerequisites

- Node.js 18+ 
- Python 3.8+
- Tesseract OCR (for Windows, download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki))

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR:**
   - Download and install Tesseract from [here](https://github.com/UB-Mannheim/tesseract/wiki)
   - Add Tesseract to your PATH, or set `TESSERACT_CMD` environment variable

5. **Run the FastAPI server:**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies:**
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
3. Click "Process Bill" to extract data
4. View the extracted information:
   - Dates found in the bill
   - Items with quantities and prices
   - Total calculated amount
   - Raw OCR text

## API Endpoints

### `POST /process-bill`
Process a bill image and extract structured data.

**Request:**
- `file`: Image file (multipart/form-data)

**Response:**
```json
{
  "success": true,
  "filename": "bill.jpg",
  "result": {
    "raw_text": {
      "tesseract": "...",
      "easyocr": "...",
      "combined": "..."
    },
    "extracted_data": {
      "dates": ["24.06.25"],
      "amounts": [...],
      "items": [...],
      "total_calculated": 1970.0,
      "item_count": 10
    },
    "processing_info": {
      "timestamp": "2025-06-27T...",
      "ocr_engines_used": ["tesseract", "easyocr"],
      "preprocessing_applied": true
    }
  }
}
```

### `POST /extract-text`
Extract raw text from an image without processing.

### `GET /health`
Check API health and OCR engine availability.

## Supported Formats

- **Image Types**: JPEG, PNG, BMP, TIFF
- **Max File Size**: 10MB
- **Languages**: Turkish (primary), English (secondary)

## Image Preprocessing

The system applies several preprocessing techniques for better OCR accuracy:

1. **Grayscale Conversion**: Removes color information
2. **CLAHE**: Contrast Limited Adaptive Histogram Equalization
3. **Denoising**: Removes image noise
4. **Gaussian Blur**: Slight smoothing
5. **Otsu Thresholding**: Automatic binary thresholding
6. **Morphological Operations**: Cleanup operations

## Turkish Language Features

- **Item Recognition**: Common Turkish grocery items (süt, ekmek, peynir, etc.)
- **Date Formats**: Turkish date patterns and month names
- **Currency**: Turkish Lira (TL, ₺) recognition
- **Quantities**: Turkish quantity units (kg, gr, lt, adet, etc.)

## Development

### Adding New Item Keywords
Edit the `turkish_keywords` dictionary in `backend/main.py`:

```python
'item_keywords': [
    'süt', 'ekmek', 'peynir', 'domates', 'patates',
    # Add more items here
]
```

### Improving OCR Accuracy
- Adjust preprocessing parameters in `preprocess_image()`
- Fine-tune OCR engine configurations
- Add more language-specific patterns

## Troubleshooting

### Common Issues

1. **Tesseract not found:**
   - Install Tesseract OCR
   - Add to PATH or set `TESSERACT_CMD` environment variable

2. **CORS errors:**
   - Ensure backend is running on port 8000
   - Check CORS settings in `backend/main.py`

3. **OCR accuracy issues:**
   - Try different image formats
   - Ensure good image quality (clear, well-lit)
   - Check if text is in Turkish or English

4. **Installation issues:**
   - Use `--legacy-peer-deps` for npm install
   - Ensure Python 3.8+ is installed
   - Check virtual environment activation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Tesseract OCR project
- EasyOCR project
- FastAPI framework
- Next.js framework
