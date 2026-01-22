import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    MODEL_NAME = "gemini-2.5-flash"
    WAKE_WORD = "bob"

    if not GOOGLE_API_KEY:
        raise ValueError("Error: No LLM API Key found in .env file")