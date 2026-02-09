# Kordiam Excel Importer - GUI Version

## 🎯 Easy-to-Use Graphical Interface

No more command line! Just double-click and use the simple interface.

## 🚀 Quick Start

### Option 1: Double-Click (Easiest)
1. **Double-click** `Kordiam Importer.bat`
2. The GUI will open automatically
3. Follow the on-screen instructions

### Option 2: Manual Launch
1. **Double-click** `run_gui.bat`
2. Or run: `python kordiam_importer_gui.py`

## 📋 How to Use the GUI

### Step 1: Set Up Files
- **Excel File**: Click "Browse" to select your Excel file
- **Mapping File**: Usually `kordiam_mapping_clean.json` (pre-filled)
- **Config File**: Usually `config.json` (pre-filled)

### Step 2: Create Example Data (Optional)
- Click **"Create Example Data"** to generate a sample Excel file
- This helps you understand the required format

### Step 3: Test Your Import
- Click **"Test Import (Dry Run)"** to test without creating elements
- Check the log output for any issues

### Step 4: Run Actual Import
- Uncheck "Dry Run" if you want to create real elements
- Click **"Run Import"** to create elements in Kordiam
- Confirm when prompted

## 🎛️ GUI Features

### File Selection
- **Browse buttons** for easy file selection
- **Auto-detection** of common file names
- **File validation** before import

### Options
- **Dry Run checkbox** - Test without creating elements
- **Real-time log** - See what's happening
- **Status bar** - Current operation status

### Buttons
- **Create Example Data** - Generate sample Excel file
- **Test Import** - Dry run with current settings
- **Run Import** - Actual import to Kordiam
- **Clear Log** - Clear the log output

## 📊 Log Output

The GUI shows real-time information:
- ✅ Success messages
- ⚠️ Warnings
- ✗ Error messages
- Import progress and results

## 🔧 Troubleshooting

### GUI Won't Start
1. Make sure Python is installed
2. Run: `pip install -r requirements.txt`
3. Check all files are in the same folder

### Import Errors
1. Check your `config.json` credentials
2. Verify Excel file format matches the mapping
3. Try the "Create Example Data" button first

### File Not Found
1. Use the "Browse" buttons to select files
2. Make sure files exist in the specified locations
3. Check file permissions

## 💡 Tips

- **Always test with dry run first**
- **Use the example data** to understand the format
- **Check the log** for detailed information
- **Keep the GUI open** during import to see progress

## 🆚 GUI vs Command Line

| Feature | GUI | Command Line |
|---------|-----|--------------|
| Ease of use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| File selection | Browse buttons | Type paths |
| Real-time feedback | ✅ | ✅ |
| Batch processing | ✅ | ✅ |
| Advanced options | Limited | Full control |

**For most users, the GUI is the best choice!** 🎉 