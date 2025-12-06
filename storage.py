# storage.py — Google Sheets Backend

import os
import json
import pandas as pd
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials


# ======================
# Load credentials
# ======================

# Read service account JSON from Streamlit Secrets variable (string)
google_key_raw = os.getenv("GOOGLE_SHEETS_KEY")

if not google_key_raw:
    raise ValueError("GOOGLE_SHEETS_KEY not found. Check Streamlit Secrets.")

service_account_info = json.loads(google_key_raw)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

client = gspread.authorize(creds)


# ======================
# Google Sheet settings
# ======================

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")  # Sheet ID from Streamlit Secrets
SHEET_NAME = "Sheet1"  # or whatever your tab name is

if not SHEET_ID:
    raise ValueError("GOOGLE_SHEET_ID not found. Add it to Secrets.")

sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)


# ======================
# Functions
# ======================

def append_submission(rating, review, ai_response, ai_summary, ai_actions):
    """Append one row of feedback to Google Sheets."""

    timestamp = datetime.utcnow().isoformat()

    row = [
        timestamp,
        rating,
        review,
        ai_response,
        ai_summary,
        ai_actions,
    ]

    sheet.append_row(row)


def load_submissions():
    """Load Google Sheets data into a pandas DataFrame."""

    records = sheet.get_all_records()

    if not records:
        return pd.DataFrame(
            columns=["timestamp", "rating", "review", "ai_response", "ai_summary", "ai_actions"]
        )

    df = pd.DataFrame(records)
    return df
