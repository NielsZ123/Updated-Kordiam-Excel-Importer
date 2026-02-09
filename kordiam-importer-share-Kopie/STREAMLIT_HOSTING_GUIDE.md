# Streamlit Hosting Guide for Kordiam Excel Importer

This guide explains how to host your Kordiam Excel Importer application on Streamlit Cloud (streamlit.io).

## Prerequisites

1. **GitHub Account**: Streamlit Cloud requires your code to be in a GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io) (free tier available)
3. **Kordiam API Credentials**: Your `client_id` and `client_secret` for OAuth2 authentication

## Step-by-Step Hosting Instructions

### 1. Prepare Your Repository

#### Option A: If you already have a GitHub repository
1. Make sure all your files are committed and pushed to GitHub
2. Ensure `requirements.txt` includes `streamlit>=1.28.0`

#### Option B: If you need to create a new repository
```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit: Kordiam Excel Importer with Streamlit"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2. Create Streamlit Cloud Account

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in" and authorize with your GitHub account
3. You'll be redirected to your Streamlit Cloud dashboard

### 3. Deploy Your App

1. **Click "New app"** in the Streamlit Cloud dashboard
2. **Select your repository** from the dropdown
3. **Configure the app**:
   - **Main file path**: `kordiam-importer-share/kordiam_importer_streamlit.py`
   - **Python version**: Select Python 3.9 or higher (recommended: 3.11)
   - **Branch**: `main` (or your default branch)

### 4. Configure Secrets (OAuth Credentials)

**IMPORTANT**: Never commit your OAuth credentials to GitHub! Use Streamlit Secrets instead.

1. In your Streamlit Cloud app dashboard, click **"⋮" (three dots)** → **"Settings"**
2. Go to **"Secrets"** tab
3. Add your credentials in TOML format:

```toml
[KORDIAM]
CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"
BASE_URL = "https://kordiam.app"
TOKEN_ENDPOINT = "/api/token"
TIMEOUT = 30
```

4. Click **"Save"**

### 5. Update Streamlit App to Use Secrets

The current `kordiam_importer_streamlit.py` expects uploaded config files. For Streamlit Cloud, you should modify it to use secrets. Here's what needs to be updated:

**Current approach**: Users upload config.json files
**Recommended for Cloud**: Use Streamlit secrets + optional config file upload

The app will need to:
1. First try to load from Streamlit secrets
2. Fall back to uploaded config file if secrets aren't available
3. Show a warning if neither is available

### 6. Deploy and Test

1. After configuring secrets, your app will automatically redeploy
2. Wait for the deployment to complete (usually 1-2 minutes)
3. Click **"Open app"** to test
4. Upload your Excel, mapping, and config files (or use secrets)

## File Structure Requirements

Your repository should have this structure:

```
your-repo/
├── kordiam-importer-share/
│   ├── kordiam_importer_streamlit.py  # Main Streamlit app
│   ├── kordiam_excel_importer.py      # Core importer logic
│   ├── create_kordiam_example_clean.py
│   ├── requirements.txt               # Must include streamlit
│   ├── config_template.json           # Template (no real credentials)
│   ├── kordiam_mapping_clean.json     # Mapping configuration
│   └── README.md
└── README.md (optional)
```

## Security Best Practices

### ✅ DO:
- Use Streamlit Secrets for OAuth credentials
- Keep `config_template.json` with placeholder values
- Use environment variables in production
- Test with dry-run mode first

### ❌ DON'T:
- Commit real credentials to GitHub
- Hardcode secrets in your Python files
- Share your Streamlit secrets publicly
- Use production credentials for testing

## Updating Your Streamlit App for Cloud Deployment

The current app requires users to upload config files. For better cloud deployment, consider updating `kordiam_importer_streamlit.py` to:

1. **Check Streamlit secrets first**:
```python
import streamlit as st

# Try to load from secrets
if 'KORDIAM' in st.secrets:
    config = {
        'base_url': st.secrets['KORDIAM']['BASE_URL'],
        'client_id': st.secrets['KORDIAM']['CLIENT_ID'],
        'client_secret': st.secrets['KORDIAM']['CLIENT_SECRET'],
        'token_endpoint': st.secrets['KORDIAM'].get('TOKEN_ENDPOINT', '/api/token'),
        'timeout': int(st.secrets['KORDIAM'].get('TIMEOUT', '30'))
    }
else:
    # Fall back to uploaded config file
    if config_file:
        config = load_config(config_path)
    else:
        st.error("Please configure Streamlit secrets or upload a config file")
        st.stop()
```

2. **Make config file upload optional** if secrets are available

## Running Locally

To test your Streamlit app locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
cd kordiam-importer-share
streamlit run kordiam_importer_streamlit.py
```

The app will open at `http://localhost:8501`

## Troubleshooting

### App won't deploy
- Check that `requirements.txt` includes `streamlit`
- Verify the main file path is correct
- Check Python version compatibility

### Authentication errors
- Verify secrets are correctly configured
- Check that credentials are valid
- Ensure BASE_URL matches your Kordiam instance

### File upload issues
- Streamlit Cloud has file size limits (200MB per file)
- Large Excel files may timeout - consider chunking

### Import errors
- Check that all dependencies are in `requirements.txt`
- Verify Python version matches your local environment
- Review deployment logs in Streamlit Cloud dashboard

## Streamlit Cloud Limits (Free Tier)

- **App sleep**: Apps sleep after 7 days of inactivity
- **File size**: 200MB per file upload
- **Memory**: 1GB RAM
- **CPU**: Shared resources
- **Bandwidth**: Reasonable use policy

## Alternative: Self-Hosting

If you prefer to host on your own server:

1. **Install Streamlit**:
```bash
pip install streamlit
```

2. **Run with systemd/PM2**:
```bash
streamlit run kordiam_importer_streamlit.py --server.port 8501
```

3. **Use reverse proxy** (nginx/Apache) for HTTPS

4. **Set environment variables** instead of secrets:
```bash
export KORDIAM_CLIENT_ID="your_id"
export KORDIAM_CLIENT_SECRET="your_secret"
```

## Next Steps

1. ✅ Add Streamlit to `requirements.txt` (already done)
2. ✅ Push code to GitHub
3. ✅ Create Streamlit Cloud account
4. ✅ Deploy app
5. ✅ Configure secrets
6. ✅ Test with dry-run mode
7. ✅ Share your app URL with users

## Support

- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-cloud
- Streamlit Community: https://discuss.streamlit.io
- Your app logs: Available in Streamlit Cloud dashboard under "Manage app" → "Logs"
