import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def get_client() -> genai.Client:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing from .env")
    return genai.Client(api_key=api_key)