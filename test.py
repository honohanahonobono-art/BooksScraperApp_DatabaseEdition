import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

print("API KEY:", GOOGLE_BOOKS_API_KEY[:6], "...")