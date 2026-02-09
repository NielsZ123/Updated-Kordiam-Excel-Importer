# 🚀 Kordiam Excel Importer - Quick Start

## 🎯 What You Have

This folder contains everything you need to import Excel data into Kordiam!

## ⚡ Super Quick Start (GUI - Recommended)

1. **Double-click** `Kordiam Importer.bat`
2. **Create your config.json** from `config_template.json`
3. **Add your Kordiam credentials** to `config.json`
4. **Click "Create Example Data"** to see the format
5. **Click "Test Import"** to test
6. **Click "Run Import"** when ready

## 📋 What's Included

### 🖥️ GUI Application
- `Kordiam Importer.bat` - **Double-click this to start!**
- `kordiam_importer_gui.py` - GUI application
- `run_gui.bat` - Alternative launcher

### 📁 Configuration Files
- `kordiam_mapping_clean.json` - Field mappings (clean version)
- `config_template.json` - Template for your credentials
- `requirements.txt` - Python packages needed

### 📊 Example Data
- `create_kordiam_example_clean.py` - Creates example Excel file
- `kordiam_example_clean.xlsx` - Sample data (already created)

### 📚 Documentation
- `SETUP_GUIDE.md` - Detailed setup instructions
- `GUI_README.md` - GUI-specific instructions
- `README.md` - Full documentation

### 🔧 Setup Tools
- `install_and_test.bat` - Windows setup script

## 🛠️ Setup Steps

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Your Config File
1. Copy `config_template.json` to `config.json`
2. Edit `config.json` with your credentials:
```json
{
  "base_url": "https://kordiam.app",
  "client_id": "YOUR_ACTUAL_CLIENT_ID",
  "client_secret": "YOUR_ACTUAL_CLIENT_SECRET",
  "token_endpoint": "/api/token",
  "timeout": 30
}
```

### 3. Test Everything
1. Double-click `Kordiam Importer.bat`
2. Click "Create Example Data"
3. Click "Test Import (Dry Run)"
4. Check the log for success messages

## 🎮 Using the GUI

### File Selection
- **Excel File**: Your data file (use example first)
- **Mapping File**: `kordiam_mapping_clean.json` (pre-filled)
- **Config File**: `config.json` (pre-filled)

### Buttons
- **Create Example Data** - Generates sample Excel file
- **Test Import** - Dry run (safe, no real data created)
- **Run Import** - Actual import to Kordiam
- **Clear Log** - Clears the log output

## 📊 Excel File Format

Your Excel file needs these columns:
- `Title` - Element title
- `Slug` - URL slug
- `Element Status` - Status ID (e.g., 2)
- `Task Status ID` - Task status (e.g., 2)
- `Task Format ID` - Format ID (e.g., 18)
- `Assigned User ID` - User ID (e.g., 10126151)
- `Task Deadline` - Deadline date/time
- `Confirmation Status` - Confirmation status (e.g., -2)
- `Platform ID` - Platform ID (e.g., 9413781)
- `Publication Date` - Publication date
- `Task Assignments` - Assignments (e.g., "true")
- `Group IDs` - Group ID (e.g., 9455121)

## 🆘 Need Help?

1. **Check the logs** in the GUI
2. **Read SETUP_GUIDE.md** for detailed instructions
3. **Use the example data** to understand the format
4. **Always test with dry run first**

## 🎉 Success!

Once you see "Import completed: Success: X, Errors: 0" in the log, your data has been successfully imported to Kordiam!

---

**Happy importing! 🚀** 