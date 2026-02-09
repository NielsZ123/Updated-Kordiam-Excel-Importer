# Kordiam Excel Importer - Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation Steps

### 1. Clone or Download the Folder
Copy the entire `kordiam importer` folder to your computer.

### 2. Navigate to the Folder
```bash
cd "path/to/kordiam importer"
```

### 3. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 5. Install Required Packages
```bash
pip install pandas openpyxl requests
```

### 6. Configure Your Credentials

**Option A: Using config.json (Recommended)**
1. Rename `config_template.json` to `config.json`
2. Edit `config.json` and replace:
   - `YOUR_CLIENT_ID_HERE` with your actual Kordiam client ID
   - `YOUR_CLIENT_SECRET_HERE` with your actual Kordiam client secret

**Option B: Using Command Line**
You can provide credentials directly when running the script (see usage examples below).

### 7. Prepare Your Excel File
- Use the column names specified in `kordiam_mapping.json`
- Ensure your Excel file has at least one of: tasks, publications, or groups
- See `create_kordiam_example.py` for an example of proper data structure

## Usage Examples

### Test Run (Dry Run)
```bash
python kordiam_excel_importer.py your_file.xlsx --mapping kordiam_mapping.json --dry-run
```

### Actual Import
```bash
python kordiam_excel_importer.py your_file.xlsx --mapping kordiam_mapping.json
```

### Using Command Line Credentials
```bash
python kordiam_excel_importer.py your_file.xlsx --mapping kordiam_mapping.json --client-id YOUR_ID --client-secret YOUR_SECRET
```

## Troubleshooting

### Common Issues:
1. **Import Error**: Make sure you have the required packages installed
2. **Authentication Error**: Check your client ID and secret
3. **Excel Reading Error**: Ensure your Excel file has the correct column names
4. **Validation Error**: Make sure your data includes at least one task, publication, or group

### Getting Help:
- Check the log files created in the same directory
- Use `--dry-run` to test without creating actual elements
- Review the `kordiam_mapping.json` file for field mappings

## File Structure
```
kordiam importer/
├── kordiam_excel_importer.py           # Main script
├── kordiam_mapping.json                # Complete field mappings (all possible fields)
├── kordiam_mapping_clean.json          # Clean field mappings (only tested fields)
├── config_template.json                # Template for credentials
├── create_kordiam_example.py           # Complete example data generator
├── create_kordiam_example_clean.py     # Clean example data generator
├── README.md                           # Detailed documentation
├── SETUP_GUIDE.md                      # This file
└── requirements.txt                    # Python package dependencies
```

## Mapping Files

**kordiam_mapping.json** - Complete mapping with all possible Kordiam fields
- Use this if you need advanced features like external links, CMS integration, etc.
- More complex but offers full functionality

**kordiam_mapping_clean.json** - Clean mapping with only tested fields
- Use this for simple imports with basic functionality
- Matches the structure that was successfully tested
- Recommended for most users 