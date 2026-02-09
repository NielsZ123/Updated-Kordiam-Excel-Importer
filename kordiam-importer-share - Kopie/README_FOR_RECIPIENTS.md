# 🎉 Welcome to the Kordiam Excel Importer!

## 🚀 You're Ready to Import Excel Data to Kordiam!

This package contains everything you need to import Excel files directly into Kordiam using a simple GUI interface.

## 📦 What You Received

### 🎯 Main Files
- **`Kordiam Importer.bat`** ← **Double-click this to start!**
- **`kordiam_importer_gui.py`** - The GUI application
- **`kordiam_excel_importer.py`** - The main import script

### 📋 Configuration
- **`kordiam_mapping_clean.json`** - Field mappings (clean version)
- **`config_template.json`** - Template for your credentials
- **`requirements.txt`** - Python packages needed

### 📊 Examples & Documentation
- **`kordiam_example_clean.xlsx`** - Sample Excel file
- **`create_kordiam_example_clean.py`** - Creates more examples
- **`QUICK_START.md`** - This quick start guide
- **`SETUP_GUIDE.md`** - Detailed setup instructions
- **`GUI_README.md`** - GUI-specific instructions

### 🔧 Setup Tools
- **`install_and_test.bat`** - Windows setup script
- **`run_gui.bat`** - Alternative GUI launcher

## ⚡ Super Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Credentials
1. Copy `config_template.json` to `config.json`
2. Edit `config.json` with your Kordiam credentials:
```json
{
  "base_url": "https://kordiam.app",
  "client_id": "YOUR_ACTUAL_CLIENT_ID",
  "client_secret": "YOUR_ACTUAL_CLIENT_SECRET",
  "token_endpoint": "/api/token",
  "timeout": 30
}
```

### Step 3: Start Using
1. **Double-click** `Kordiam Importer.bat`
2. **Click "Create Example Data"** to see the format
3. **Click "Test Import"** to test safely
4. **Click "Run Import"** when ready

## 🎮 Using the GUI

The GUI makes it super easy:

### File Selection
- **Excel File**: Your data file (browse to select)
- **Mapping File**: `kordiam_mapping_clean.json` (pre-filled)
- **Config File**: `config.json` (pre-filled)

### Buttons
- **Create Example Data** - Generates sample Excel file
- **Test Import** - Safe dry run (no real data created)
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

1. **Check the logs** in the GUI for detailed information
2. **Read QUICK_START.md** for step-by-step instructions
3. **Use the example data** to understand the format
4. **Always test with dry run first**

## 🎉 Success Indicators

When you see this in the log:
```
✓ Import completed!
Success: 3
Errors: 0
```

Your data has been successfully imported to Kordiam! 🚀

## 💡 Pro Tips

- **Start with the example data** to understand the format
- **Use dry run first** to test without creating real elements
- **Check publication dates** match your platform schedule
- **Keep the GUI open** during import to see progress

## 🔒 Security Note

- Never share your `config.json` file (contains your credentials)
- The `config_template.json` is safe to share
- Always use dry run to test before real imports

---

**Happy importing! Your Kordiam Excel Importer is ready to use! 🎯** 