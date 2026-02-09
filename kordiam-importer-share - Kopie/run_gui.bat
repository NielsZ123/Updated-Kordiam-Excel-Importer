@echo off
echo ========================================
echo Kordiam Excel Importer - GUI Launcher
echo ========================================
echo.

echo Starting GUI application...
python kordiam_importer_gui.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start GUI application
    echo.
    echo Possible solutions:
    echo 1. Make sure Python is installed
    echo 2. Install required packages: pip install -r requirements.txt
    echo 3. Make sure all files are in the same directory
    echo.
    pause
) 