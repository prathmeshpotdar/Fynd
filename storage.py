import os
import json
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

google_key_raw = os.getenv("GOOGLE_SHEETS_KEY")

if not google_key_raw:
    raise ValueError("GOOGLE_SHEETS_KEY not found in Streamlit Secrets")

# Load JSON directly
service_account_info = json.loads(google_key_raw)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

client = gspread.authorize(creds)

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
sheet = client.open_by_key(SHEET_ID).sheet1
