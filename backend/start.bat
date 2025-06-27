@echo off
echo Starting Turkish Bill OCR Backend...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements if they don't exist
if not exist "venv\Lib\site-packages\fastapi\" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Start the server
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.
python main.py
