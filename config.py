"""
Configuration file for Enterprise Attendance System
Store all configuration variables here

IMPORTANT FOR GITHUB USERS:
- DO NOT commit your actual n8n URL to GitHub
- Use Streamlit Secrets for sensitive data
- See README.md for setup instructions
"""

import os
from typing import Literal

# Import streamlit only when needed to avoid circular imports
try:
    import streamlit as st

    _has_streamlit = True
except ImportError:
    _has_streamlit = False

# ============================================================================
# SECURITY: n8n Configuration
# ============================================================================
# For local development: Create .streamlit/secrets.toml with your n8n URL
# For production: Use Streamlit Cloud Secrets
#
# GitHub Users: This file has placeholders. Add your actual values to secrets.toml
# Format: https://your-n8n-domain.com/webhook
# ============================================================================

# Try to get n8n URL from Streamlit secrets first
N8N_BASE_URL = "YOUR_N8N_URL_HERE"  # Default placeholder

if _has_streamlit:
    try:
        N8N_BASE_URL = st.secrets["n8n"]["base_url"]
    except (KeyError, FileNotFoundError, AttributeError):
        # Try environment variable
        N8N_BASE_URL = os.getenv('N8N_BASE_URL', 'YOUR_N8N_URL_HERE')
else:
    N8N_BASE_URL = os.getenv('N8N_BASE_URL', 'YOUR_N8N_URL_HERE')

# ============================================================================
# Google Sheets Configuration
# ============================================================================
# GitHub Users: Add your Google Sheet ID to secrets.toml
# Found in URL: docs.google.com/spreadsheets/d/[THIS_IS_THE_ID]/edit
# ============================================================================

GOOGLE_SHEET_ID = "YOUR_SHEET_ID_HERE"  # Default placeholder

if _has_streamlit:
    try:
        GOOGLE_SHEET_ID = st.secrets["google_sheets"]["sheet_id"]
    except (KeyError, FileNotFoundError, AttributeError):
        GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', 'YOUR_SHEET_ID_HERE')
else:
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', 'YOUR_SHEET_ID_HERE')

# ============================================================================
# Application Settings
# ============================================================================
# These are safe to keep as-is or customize for your needs
DEFAULT_NEXT_EMPLOYEE_ID = 21  # Starting employee ID number
WORKING_HOURS_PER_DAY = 8
TAX_RATE = 0.15  # 15% tax
LATE_CUTOFF_TIME = "09:30"  # Late after 9:30 AM

# ============================================================================
# Department Options
# ============================================================================
# GitHub Users: Customize this list for your organization
DEPARTMENTS = [
    "IT",
    "HR",
    "Finance",
    "Marketing",
    "Sales",
    "Operations",
    "Customer Service"
]

# ============================================================================
# Default Hourly Rates (optional - customize or remove)
# ============================================================================
DEFAULT_HOURLY_RATES = {
    'E001': 25.00,
    'E002': 20.00,
    'E003': 28.00,
    'E004': 22.00,
    'E005': 30.00,
    # Add more as needed
}

# ============================================================================
# API Settings
# ============================================================================
API_TIMEOUT = 10  # seconds
MAX_RETRIES = 3

# ============================================================================
# UI Settings
# ============================================================================
PAGE_TITLE = "Enterprise Attendance System"
PAGE_ICON = "📊"
LAYOUT: Literal["centered", "wide"] = "wide"

# ============================================================================
# Feature Flags
# ============================================================================
ENABLE_SIDEBAR_CONFIG = False  # Set to False to hide n8n URL config in sidebar
ENABLE_DEBUG_MODE = False  # Set to True to show debug information


# ============================================================================
# Validation
# ============================================================================
def validate_config():
    """Validate that required configuration is set"""
    import streamlit as st

    errors = []

    if N8N_BASE_URL == "YOUR_N8N_URL_HERE" or not N8N_BASE_URL:
        errors.append("⚠️ N8N_BASE_URL not configured.")

    if GOOGLE_SHEET_ID == "YOUR_SHEET_ID_HERE" or not GOOGLE_SHEET_ID:
        errors.append("⚠️ GOOGLE_SHEET_ID not configured.")

    if errors:
        st.error("**Configuration Missing**")
        for error in errors:
            st.error(error)

        st.info("""
        **How to fix:**

        1. Create file: `.streamlit/secrets.toml` in your project folder

        2. Add this content (replace with your actual values):

        ```toml
        [n8n]
        base_url = "https://n8n_URL/webhook"

        [google_sheets]
        sheet_id = "SHEET_ID"
        ```

        3. Save the file and restart: `streamlit run main.py`
        """)
        st.stop()

    return errors

# ============================================================================
# GitHub Users - Quick Setup Checklist:
# ============================================================================
# 1. Replace N8N_BASE_URL with your n8n webhook URL (or use secrets)
# 2. Replace GOOGLE_SHEET_ID with your Google Sheet ID
# 3. Customize DEPARTMENTS list if needed
# 4. For Streamlit Cloud: Create secrets.toml file (see example below)
# 5. For security: Never commit actual URLs to public repos
# ============================================================================
