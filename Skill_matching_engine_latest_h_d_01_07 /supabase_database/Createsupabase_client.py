from supabase import create_client
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_PATH = os.path.join(BASE_DIR, ".env")

print("CURRENT =", BASE_DIR)
print("ENV_PATH =", ENV_PATH)

load_dotenv(ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL =", SUPABASE_URL)
print("KEY FOUND =", "YES" if SUPABASE_KEY else "NO")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)