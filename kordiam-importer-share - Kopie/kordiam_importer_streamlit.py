#!/usr/bin/env python3
"""
Kordiam Excel Importer - Streamlit Version
Web-based GUI for importing Excel data to Kordiam.
"""

import streamlit as st
import json
import os
from datetime import datetime
import tempfile
import io
import pandas as pd
from kordiam_excel_importer import KordiamImporter, load_config, KordiamConfig


# Streamlit page setup
st.set_page_config(page_title="Kordiam Excel Importer", layout="wide")
 
FIELD_DEFINITIONS = [
    # (section, label, kordiam_field, field_type)
    ("element_fields", "Title", "title", "text"),
    ("element_fields", "Slug", "slug", "text"),
    ("element_fields", "Element Status", "elementStatus", "id"),
    ("tasks", "Task Status ID", "status", "id"),
    ("tasks", "Task Format ID", "format", "id"),
    ("tasks", "Assigned User ID", "user", "id"),
    ("tasks", "Task Deadline", "deadline", "datetime"),
    ("tasks", "Confirmation Status", "confirmationStatus", "id"),
    ("publications", "Platform ID", "platform", "id"),
    ("publications", "Publication Date", "single", "date"),
    ("publications", "Task Assignments", "assignments", "bool"),
    ("groups", "Group IDs", "id", "group_ids"),
    ("event", "Event Start Date", "fromDate", "date"),
    ("event", "Event Start Time", "fromTime", "time"),
    ("event", "Event End Date", "toDate", "date"),
    ("event", "Event End Time", "toTime", "time"),
]
st.title("📊 Kordiam Excel Importer")


# --- Load Configuration from Secrets or File ---
def get_config_from_secrets_or_file(config_file=None):
    """
    Try to load config from Streamlit secrets first, then fall back to uploaded file.
    Returns KordiamConfig object or None.
    
    Args:
        config_file: Streamlit uploaded file object or file path string
    """
    # Try Streamlit secrets first (recommended for cloud deployment)
    try:
        if 'KORDIAM' in st.secrets:
            log_message("Loading configuration from Streamlit secrets...")
            return KordiamConfig(
                base_url=st.secrets['KORDIAM'].get('BASE_URL', 'https://kordiam.app'),
                client_id=st.secrets['KORDIAM']['CLIENT_ID'],
                client_secret=st.secrets['KORDIAM']['CLIENT_SECRET'],
                token_endpoint=st.secrets['KORDIAM'].get('TOKEN_ENDPOINT', '/api/token'),
                timeout=int(st.secrets['KORDIAM'].get('TIMEOUT', '30'))
            )
    except Exception as e:
        log_message(f"Could not load from secrets: {e}")
    
    # Fall back to uploaded config file
    if config_file:
        try:
            log_message("Loading configuration from uploaded file...")
            # If it's a Streamlit uploaded file, save to temp file first
            if hasattr(config_file, 'read'):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as tmp_config:
                    config_file.seek(0)  # Reset file pointer
                    tmp_config.write(config_file.read().decode('utf-8'))
                    config_path = tmp_config.name
            else:
                config_path = config_file
            
            return load_config(config_path)
        except Exception as e:
            log_message(f"Could not load from config file: {e}")
            raise
    
    return None


# --- Session State for Logs ---
if "logs" not in st.session_state:
    st.session_state.logs = ""

def log_message(message: str):
    """Append a log message with timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs += f"[{timestamp}] {message}\n"


# --- Sidebar Options ---
st.sidebar.header("⚙️ Options")
dry_run = st.sidebar.checkbox("Dry Run (Test without creating elements)", value=True)
mapping_source = st.sidebar.radio(
    "Mapping Source",
    ["Build from Excel columns", "Upload mapping JSON"],
    index=0
)


# --- Configuration Status ---
config_available = False
try:
    if 'KORDIAM' in st.secrets:
        config_available = True
        st.sidebar.success("✅ Config loaded from Streamlit secrets")
except:
    pass

# --- File Selection ---
st.header("📂 File Selection")

excel_file = st.file_uploader("Select Excel File", type=["xlsx", "xls"])
mapping_file = None
if mapping_source == "Upload mapping JSON":
    mapping_file = st.file_uploader("Select Mapping File (JSON)", type=["json"])

# Config file is optional if secrets are available
if config_available:
    st.info("💡 Config file is optional - using Streamlit secrets. You can still upload a config file to override.")
    config_file = st.file_uploader("Select Config File (JSON) - Optional", type=["json"])
else:
    config_file = st.file_uploader("Select Config File (JSON)", type=["json"])


def get_excel_headers(uploaded_file):
    if not uploaded_file:
        return []
    data = uploaded_file.getvalue()
    df = pd.read_excel(io.BytesIO(data), nrows=0)
    return [str(c) for c in df.columns]


def build_mapping_from_selections(selections):
    mapping_config = {
        "element_fields": {},
        "tasks": {},
        "publications": {},
        "groups": {},
        "event": {}
    }

    for section, _, kordiam_field, _ in FIELD_DEFINITIONS:
        selected = selections.get((section, kordiam_field))
        if selected and selected != "(none)":
            mapping_config[section][selected] = kordiam_field

    return {k: v for k, v in mapping_config.items() if v}


# --- Buttons for Actions ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📑 Create Example Data"):
        try:
            import create_kordiam_example_clean
            log_message("✓ Example data created successfully! File: kordiam_example_clean.xlsx")
            st.success("Example data created: kordiam_example_clean.xlsx")
        except Exception as e:
            log_message(f"✗ Error creating example data: {e}")
            st.error(f"Error creating example data: {e}")


def run_import(excel_file, mapping_file, config_file, dry_run: bool):
    """Run importer and log results."""
    try:
        if not excel_file:
            raise ValueError("Please select an Excel file")
        if mapping_source == "Upload mapping JSON" and not mapping_file:
            raise ValueError("Please select a Mapping file")
        
        # Load configuration (from secrets or file)
        log_message("Loading configuration...")
        config = get_config_from_secrets_or_file(config_file)
        
        if not config:
            raise ValueError("No configuration available. Please configure Streamlit secrets or upload a config file.")

        # Save uploaded files to temp dir (since importer expects file paths)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_excel:
            tmp_excel.write(excel_file.getvalue())
            excel_path = tmp_excel.name

        if mapping_source == "Upload mapping JSON":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_mapping:
                tmp_mapping.write(mapping_file.getvalue())
                mapping_path = tmp_mapping.name

            log_message("Loading mapping configuration...")
            with open(mapping_path, 'r') as f:
                mapping_config = json.load(f)
        else:
            mapping_config = st.session_state.get("built_mapping_config")
            if not mapping_config:
                raise ValueError("No mapping selections found. Choose Excel columns or upload a mapping JSON.")

        # Create importer
        importer = KordiamImporter(config)

        # Run import
        operation = "dry run" if dry_run else "import"
        log_message(f"Starting {operation}...")

        results = importer.import_from_excel(
            excel_file=excel_path,
            mapping_config=mapping_config,
            dry_run=dry_run
        )

        log_message(f"✓ {operation.capitalize()} completed!")
        log_message(f"Success: {results['success']}")
        log_message(f"Errors: {results['errors']}")

        if results['errors'] > 0:
            log_message("⚠ Some errors occurred. Check details above.")

        st.success(f"{operation.capitalize()} completed: {results['success']} success, {results['errors']} errors")

    except Exception as e:
        log_message(f"✗ Error during import: {e}")
        st.error(f"Error during import: {e}")


with col2:
    if st.button("🧪 Test Import (Dry Run)"):
        if excel_file and (mapping_file or mapping_source == "Build from Excel columns"):
            # Check if config is available (secrets or file)
            try:
                test_config = get_config_from_secrets_or_file(config_file)
                if not test_config:
                    st.error("❌ No configuration available. Please configure Streamlit secrets or upload a config file.")
                else:
                    log_message("=== Starting Test Import (Dry Run) ===")
                    run_import(excel_file, mapping_file, config_file, dry_run=True)
            except Exception as e:
                st.error(f"Configuration error: {e}")
        else:
            log_message("⚠ Please select Excel and Mapping files.")
            st.warning("Please upload Excel and Mapping files first.")

with col3:
    if st.button("🚀 Run Import"):
        if excel_file and (mapping_file or mapping_source == "Build from Excel columns"):
            # Check if config is available (secrets or file)
            try:
                test_config = get_config_from_secrets_or_file(config_file)
                if not test_config:
                    st.error("❌ No configuration available. Please configure Streamlit secrets or upload a config file.")
                else:
                    log_message("=== Starting Actual Import ===")
                    run_import(excel_file, mapping_file, config_file, dry_run=dry_run)
            except Exception as e:
                st.error(f"Configuration error: {e}")
        else:
            log_message("⚠ Please select Excel and Mapping files.")
            st.warning("Please upload Excel and Mapping files first.")

with col4:
    if st.button("🧹 Clear Log"):
        st.session_state.logs = ""


# --- Log Output ---
st.subheader("📜 Log Output")
st.text_area("Logs", st.session_state.logs, height=300)


# --- Mapping Builder UI ---
if mapping_source == "Build from Excel columns":
    st.header("ðŸ§­ Field Mapping Builder")

    if not excel_file:
        st.info("Upload an Excel file to load column headers.")
    else:
        try:
            headers = get_excel_headers(excel_file)
            if not headers:
                st.warning("No columns detected in Excel file.")
            else:
                selections = {}

                st.subheader("IDs")
                for section, label, kordiam_field, field_type in FIELD_DEFINITIONS:
                    if field_type not in ["id", "group_ids"]:
                        continue
                    key = (section, kordiam_field)
                    display = f"[{section}] {label}"
                    selections[key] = st.selectbox(
                        display,
                        ["(none)"] + headers,
                        key=f"id_{section}_{kordiam_field}"
                    )

                st.subheader("Dates/Times")
                for section, label, kordiam_field, field_type in FIELD_DEFINITIONS:
                    if field_type not in ["date", "time", "datetime"]:
                        continue
                    key = (section, kordiam_field)
                    display = f"[{section}] {label}"
                    selections[key] = st.selectbox(
                        display,
                        ["(none)"] + headers,
                        key=f"dt_{section}_{kordiam_field}"
                    )

                st.subheader("Text/Other")
                for section, label, kordiam_field, field_type in FIELD_DEFINITIONS:
                    if field_type in ["id", "group_ids", "date", "time", "datetime"]:
                        continue
                    key = (section, kordiam_field)
                    display = f"[{section}] {label}"
                    selections[key] = st.selectbox(
                        display,
                        ["(none)"] + headers,
                        key=f"text_{section}_{kordiam_field}"
                    )

                mapping_config = build_mapping_from_selections(selections)
                st.session_state["built_mapping_config"] = mapping_config

                if mapping_config:
                    mapping_json = json.dumps(mapping_config, indent=2)
                    st.download_button(
                        label="Download Mapping JSON",
                        data=mapping_json,
                        file_name="kordiam_mapping_custom.json",
                        mime="application/json"
                    )
                else:
                    st.info("Select at least one Excel column to build a mapping.")
        except Exception as e:
            st.error(f"Error reading Excel headers: {e}")
