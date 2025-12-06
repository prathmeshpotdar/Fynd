import os
import json
import base64
import pandas as pd
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

# ===================
# Load Base64-encoded credentials
# ===================

google_key_b64 = os.getenv("GOOGLE_SHEETS_KEY_B64")

if not google_key_b64:
    raise ValueError("GOOGLE_SHEETS_KEY_B64 missing in Streamlit Secrets.")

google_key_json = base64.b64decode(google_key_b64).decode("utf-8")
service_account_info = json.loads(google_key_json)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

client = gspread.authorize(creds)


# ===================
# Google Sheet
# ===================

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_NAME = "Sheet1"

if not SHEET_ID:
    raise ValueError("GOOGLE_SHEET_ID missing in secrets.")

sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)


# ===================
# Main functions
# ===================

def append_submission(rating, review, ai_response, ai_summary, ai_actions):
    timestamp = datetime.utcnow().isoformat()
    row = [timestamp, rating, review, ai_response, ai_summary, ai_actions]
    sheet.append_row(row)


def load_submissions():
    records = sheet.get_all_records()
    if not records:
        return pd.DataFrame(columns=["timestamp", "rating", "review", "ai_response", "ai_summary", "ai_actions"])
    return pd.DataFrame(records)
