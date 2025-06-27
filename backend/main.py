from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import cv2
import numpy as np
from PIL import Image
import io
import re
from typing import Dict, List, Optional
import logging
from datetime import datetime
import os

# Fix for Pillow compatibility issue with ANTIALIAS
try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS
except Exception:
    pass

# OCR libraries
try:
    import pytesseract
    import easyocr
    TESSERACT_AVAILABLE = True
    EASYOCR_AVAILABLE = True
except ImportError as e:
    print(f"OCR libraries not available: {e}")
    TESSERACT_AVAILABLE = False
    EASYOCR_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Turkish Bill OCR API",
    description="API for extracting data from Turkish handwritten bills",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize EasyOCR reader for Turkish
if EASYOCR_AVAILABLE:
    reader = easyocr.Reader(['tr', 'en'], gpu=False)

class BillOCR:
    def __init__(self):
        self.turkish_keywords = {
            'date_patterns': [
                r'\d{1,2}[./]\d{1,2}[./]\d{2,4}',
                r'\d{1,2}\s*(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)\s*\d{2,4}'
            ],
            'amount_patterns': [
                r'\d+[.,]\d{2}\s*(tl|₺)',
                r'\d+\s*(tl|₺)',
                r'\d+[.,]\d{2}'
            ],
            'item_keywords': [
                'süt', 'ekmek', 'peynir', 'domates', 'patates', 'soğan', 'elma', 'muz',
                'tavuk', 'et', 'balık', 'yumurta', 'yoğurt', 'tereyağı', 'zeytinyağı',
                'pirinç', 'makarna', 'fasulye', 'mercimek', 'bulgur', 'şeker', 'tuz',
                'çay', 'kahve', 'su', 'meyve', 'sebze', 'karnabahar', 'havuç', 'biber'
            ],
            'quantity_keywords': ['kg', 'gr', 'lt', 'adet', 'paket', 'kutu']
        }
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(denoised, (1, 1), 0)
        
        # Threshold to get binary image
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Morphological operations to clean up
        kernel = np.ones((1,1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text_tesseract(self, image: np.ndarray) -> str:
        """Extract text using Tesseract OCR"""
        if not TESSERACT_AVAILABLE:
            return ""
        
        try:
            # Configure Tesseract for Turkish
            config = '--oem 3 --psm 6 -l tur+eng'
            text = pytesseract.image_to_string(image, config=config)
            return text
        except Exception as e:
            logger.error(f"Tesseract OCR error: {e}")
            return ""
    
    def extract_text_easyocr(self, image: np.ndarray) -> str:
        """Extract text using EasyOCR"""
        if not EASYOCR_AVAILABLE:
            return ""
        
        try:
            results = reader.readtext(image)
            text = ' '.join([result[1] for result in results])
            return text
        except Exception as e:
            logger.error(f"EasyOCR error: {e}")
            return ""
    
    def extract_dates(self, text: str) -> List[str]:
        """Extract dates from text"""
        dates = []
        for pattern in self.turkish_keywords['date_patterns']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        return dates
    
    def extract_amounts(self, text: str) -> List[Dict]:
        """Extract monetary amounts from text"""
        amounts = []
        for pattern in self.turkish_keywords['amount_patterns']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                amount_str = match.group()
                # Clean and parse amount
                amount_clean = re.sub(r'[^\d.,]', '', amount_str)
                if amount_clean:
                    amounts.append({
                        'original': amount_str,
                        'value': amount_clean,
                        'position': match.span()
                    })
        return amounts
    
    def extract_items(self, text: str) -> List[Dict]:
        """Extract items and their details from text"""
        items = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip().lower()
            if not line:
                continue
            
            # Check if line contains item keywords
            found_items = []
            for keyword in self.turkish_keywords['item_keywords']:
                if keyword in line:
                    found_items.append(keyword)
            
            if found_items:
                # Extract quantities
                quantities = []
                for qty_keyword in self.turkish_keywords['quantity_keywords']:
                    qty_pattern = rf'\d+[.,]?\d*\s*{qty_keyword}'
                    qty_matches = re.findall(qty_pattern, line, re.IGNORECASE)
                    quantities.extend(qty_matches)
                
                # Extract amounts
                amounts = self.extract_amounts(line)
                
                items.append({
                    'line': line,
                    'items': found_items,
                    'quantities': quantities,
                    'amounts': amounts
                })
        
        return items
    
    def calculate_total(self, amounts: List[Dict]) -> Optional[float]:
        """Calculate total amount"""
        total = 0.0
        for amount in amounts:
            try:
                value_str = amount['value'].replace(',', '.')
                value = float(value_str)
                total += value
            except ValueError:
                continue
        return total if total > 0 else None
    
    def process_bill(self, image: np.ndarray) -> Dict:
        """Process bill image and extract structured data"""
        # Preprocess image
        preprocessed = self.preprocess_image(image)
        
        # Extract text using multiple OCR engines
        text_tesseract = self.extract_text_tesseract(preprocessed)
        text_easyocr = self.extract_text_easyocr(preprocessed)
        
        # Combine results (you might want to implement a more sophisticated merging strategy)
        combined_text = f"{text_tesseract}\n{text_easyocr}"
        
        # Extract structured data
        dates = self.extract_dates(combined_text)
        amounts = self.extract_amounts(combined_text)
        items = self.extract_items(combined_text)
        total = self.calculate_total(amounts)
        
        return {
            'raw_text': {
                'tesseract': text_tesseract,
                'easyocr': text_easyocr,
                'combined': combined_text
            },
            'extracted_data': {
                'dates': dates,
                'amounts': amounts,
                'items': items,
                'total_calculated': total,
                'item_count': len(items)
            },
            'processing_info': {
                'timestamp': datetime.now().isoformat(),
                'ocr_engines_used': ['tesseract', 'easyocr'],
                'preprocessing_applied': True
            }
        }

# Initialize OCR processor
ocr_processor = BillOCR()

@app.get("/")
async def root():
    return {"message": "Turkish Bill OCR API", "status": "running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ocr_available": {
            "tesseract": TESSERACT_AVAILABLE,
            "easyocr": EASYOCR_AVAILABLE
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/process-bill")
async def process_bill(file: UploadFile = File(...)):
    """Process uploaded bill image and extract data"""
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert PIL image to numpy array
        image_np = np.array(image)
        
        # Process the bill
        result = ocr_processor.process_bill(image_np)
        
        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "result": result
        })
        
    except Exception as e:
        logger.error(f"Error processing bill: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/extract-text")
async def extract_text_only(file: UploadFile = File(...)):
    """Extract raw text from uploaded image"""
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_np = np.array(image)
        
        # Preprocess
        preprocessed = ocr_processor.preprocess_image(image_np)
        
        # Extract text
        text_tesseract = ocr_processor.extract_text_tesseract(preprocessed)
        text_easyocr = ocr_processor.extract_text_easyocr(preprocessed)
        
        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "text": {
                "tesseract": text_tesseract,
                "easyocr": text_easyocr
            }
        })
        
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
