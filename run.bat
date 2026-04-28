@echo off
echo [INFO] Setting up AI Virtual Mouse...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment and install dependencies
echo [INFO] Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

:: Run the application
echo [INFO] Launching AI Virtual Mouse...
python main.py

pause
