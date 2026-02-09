@echo off
echo ========================================
echo Kordiam Excel Importer - Setup Script
echo ========================================
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Creating example data...
python create_kordiam_example_clean.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to create example data
    pause
    exit /b 1
)

echo.
echo Step 3: Testing with dry run...
python kordiam_excel_importer.py kordiam_example_clean.xlsx --mapping kordiam_mapping_clean.json --dry-run
if %errorlevel% neq 0 (
    echo ERROR: Dry run failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Copy config_template.json to config.json
echo 2. Edit config.json with your Kordiam credentials
echo 3. Run the importer with your own Excel file
echo.
echo Example command:
echo python kordiam_excel_importer.py your_file.xlsx --mapping kordiam_mapping_clean.json
echo.
pause 