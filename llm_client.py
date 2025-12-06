from dotenv import load_dotenv
load_dotenv()

import os
import json
from groq import Groq

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Please set it in your environment or .env file.")

# Groq client
client = Groq(api_key=GROQ_API_KEY)

# ✔ NEW model (FAST + cheap + perfect for this use case)
MODEL_NAME = "llama-3.1-8b-instant"


def generate_feedback(rating: int, review: str):
    """
    Uses Groq Llama 3.1 8B Instant to generate:
    - A friendly user response
    - A short summary
    - Recommended actions
    """

    system_prompt = (
        "You are an assistant for a customer feedback platform.\n"
        "Given a star rating and a short review:\n"
        "1. Generate a friendly response for the user.\n"
        "2. Summarize the review in one sentence.\n"
        "3. Suggest 1–3 recommended actions for the business.\n\n"
        "Return strictly valid JSON ONLY:\n"
        "{\n"
        "  \"user_response\": \"...\",\n"
        "  \"summary\": \"...\",\n"
        "  \"actions\": \"...\"\n"
        "}"
    )

    user_prompt = f"""
Star rating: {rating}
User review: "{review}"
"""

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.3,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
    )

    raw_output = completion.choices[0].message.content.strip()

    # Try parsing JSON safely
    try:
        data = json.loads(raw_output)
    except Exception:
        data = {
            "user_response": "Thank you for your feedback! We appreciate your time.",
            "summary": "Summary unavailable due to formatting issue.",
            "actions": "Review manually; follow up if required."
        }

    user_response = data.get("user_response", "")
    summary = data.get("summary", "")
    actions = data.get("actions", "")

    return user_response, summary, actions
