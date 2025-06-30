import os
from typing import List

class Settings:
    # Project Configuration
    PROJECT_NAME: str = "GPT-4o Bill Analysis"
    VERSION: str = "2.0.0"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.1
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    # Image Processing
    IMAGE_MAX_WIDTH: int = 2048
    IMAGE_MAX_HEIGHT: int = 2048
    IMAGE_QUALITY: int = 95
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
