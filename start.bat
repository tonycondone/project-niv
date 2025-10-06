@echo off
echo 🚀 PROJECT NIV - Starting Production Dashboard System
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is installed
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo ✅ pip is available
echo.

REM Install dependencies
echo 📦 Installing Python dependencies...
pip install -r requirement.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!
echo.

REM Run the production system
echo 🚀 Starting PROJECT NIV Production System...
echo.
python production_main.py

pause