# Quick Deploy Guide - Streamlit Cloud

## 🚀 Fast Track (5 minutes)

### 1. Push to GitHub
```bash
git add .
git commit -m "Add Streamlit support"
git push
```

### 2. Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository
4. Set **Main file path**: `kordiam-importer-share/kordiam_importer_streamlit.py`
5. Click "Deploy"

### 3. Add Secrets
1. In app settings → **Secrets**
2. Paste this (replace with your credentials):
```toml
[KORDIAM]
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
BASE_URL = "https://kordiam.app"
TOKEN_ENDPOINT = "/api/token"
TIMEOUT = "30"
```
3. Click "Save" - app will auto-redeploy

### 4. Test
- Upload Excel file
- Upload mapping JSON
- Config file is optional (secrets are used)
- Click "Test Import (Dry Run)" first!

## ✅ What's Been Updated

- ✅ Added `streamlit>=1.28.0` to `requirements.txt`
- ✅ Updated app to support Streamlit secrets
- ✅ Config file is now optional when secrets are configured
- ✅ Better error messages and status indicators

## 📚 Full Documentation

See `STREAMLIT_HOSTING_GUIDE.md` for detailed instructions.
