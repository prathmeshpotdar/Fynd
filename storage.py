# storage.py

import os
import pandas as pd
from datetime import datetime
import tempfile

# ========== IMPORTANT (FOR DEPLOYMENT) ==========
# Streamlit Cloud CANNOT write to your repo folder.
# Using tempfile.gettempdir() gives us a writable shared directory.
# ================================================

DATA_DIR = tempfile.gettempdir()
DATA_FILE = os.path.join(DATA_DIR, "submissions.csv")

COLUMNS = ["timestamp", "rating", "review", "ai_response", "ai_summary", "ai_actions"]


def ensure_storage():
    """Ensure the submissions CSV exists."""
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_FILE, index=False)


def append_submission(rating, review, ai_response, ai_summary, ai_actions):
    """Append a new row to the submissions CSV."""
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


def load_submissions():
    """Load all submissions as a DataFrame."""
    ensure_storage()
    return pd.read_csv(DATA_FILE)
