import os
import json
import base64
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Read Base64-encoded JSON key
key_b64 = os.getenv("GOOGLE_SHEETS_KEY_B64")

if not key_b64:
    raise ValueError("GOOGLE_SHEETS_KEY_B64 not found in Streamlit Secrets")

try:
    key_json = base64.b64decode(key_b64).decode("utf-8")
    service_account_info = json.loads(key_json)
except Exception as e:
    raise ValueError(f"Failed to decode service account key: {e}")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

client = gspread.authorize(creds)

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
sheet = client.open_by_key(SHEET_ID).sheet1


def append_submission(rating, review, ai_response, ai_summary, ai_actions):
    timestamp = datetime.utcnow().isoformat()
    row = [timestamp, rating, review, ai_response, ai_summary, ai_actions]
    sheet.append_row(row)


def load_submissions():
    records = sheet.get_all_records()
    if not records:
        return pd.DataFrame(
            columns=["timestamp", "rating", "review", "ai_response", "ai_summary", "ai_actions"]
        )
    return pd.DataFrame(records)
