import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

print("Listing Draft Studio starting...")
print("API key loaded:", bool(api_key))