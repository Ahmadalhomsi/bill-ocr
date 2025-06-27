import requests
import json
from pathlib import Path

def test_api_health():
    """Test if the API is running and healthy"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ API is healthy!")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print(f"❌ API health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the backend is running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error checking API health: {e}")
        return False

def test_text_extraction():
    """Test text extraction with a sample image"""
    # This would require a sample image file
    sample_image_path = Path("sample_bill.jpg")
    
    if not sample_image_path.exists():
        print("ℹ️  No sample image found. Skipping text extraction test.")
        print("   Add a sample_bill.jpg file to test OCR functionality.")
        return True
    
    try:
        with open(sample_image_path, "rb") as f:
            files = {"file": f}
            response = requests.post("http://localhost:8000/extract-text", files=files)
        
        if response.status_code == 200:
            print("✅ Text extraction test passed!")
            result = response.json()
            print(f"   Extracted text length: {len(result.get('text', {}).get('combined', ''))}")
            return True
        else:
            print(f"❌ Text extraction test failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing text extraction: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Turkish Bill OCR API...")
    print("=" * 50)
    
    # Test API health
    health_ok = test_api_health()
    print()
    
    # Test text extraction if API is healthy
    if health_ok:
        test_text_extraction()
    
    print("\n" + "=" * 50)
    print("🏁 Testing complete!")
