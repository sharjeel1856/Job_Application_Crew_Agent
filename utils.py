import os
from dotenv import load_dotenv

load_dotenv()  # loads .env

def get_openai_api_key():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not found. Put it in .env or environment.")
    return key

def get_serper_api_key():
    key = os.environ.get("SERPER_API_KEY")
    if not key:
        raise RuntimeError("SERPER_API_KEY not found. Put it in .env or environment.")
    return key
