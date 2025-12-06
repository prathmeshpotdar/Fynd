# storage.py
import os
import pandas as pd
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "submissions.csv")

COLUMNS = ["timestamp", "rating", "review", "ai_response", "ai_summary", "ai_actions"]

def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_FILE, index=False)

def append_submission(rating: int, review: str, ai_response: str, ai_summary: str, ai_actions: str):
    ensure_storage()
    new_row = {
        "timestamp": datetime.utcnow().isoformat(),
        "rating": rating,
        "review": review,
        "ai_response": ai_response,
        "ai_summary": ai_summary,
        "ai_actions": ai_actions,
    }
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def load_submissions() -> pd.DataFrame:
    ensure_storage()
    return pd.read_csv(DATA_FILE)
