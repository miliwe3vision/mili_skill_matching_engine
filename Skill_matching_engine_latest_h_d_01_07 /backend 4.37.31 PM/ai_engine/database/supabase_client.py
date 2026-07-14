import os

from dotenv import load_dotenv
from supabase import create_client

# ---------------------------------------------------
# Current directory
# backend/ai_engine/database
# ---------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------
# Project Root
# Skill_matching_engine
# ---------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        CURRENT_DIR,
        "..",   # ai_engine
        "..",   # backend
        ".."    # Skill_matching_engine
    )
)

# ---------------------------------------------------
# .env location
# ---------------------------------------------------

ENV_PATH = os.path.join(
    PROJECT_ROOT,
    "supabase_database",
    ".env"
)

print("ENV PATH :", ENV_PATH)
print("FOUND    :", os.path.exists(ENV_PATH))

load_dotenv(ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL FOUND :", bool(SUPABASE_URL))
print("KEY FOUND :", bool(SUPABASE_KEY))

if not SUPABASE_URL:
    raise Exception("SUPABASE_URL not found.")

if not SUPABASE_KEY:
    raise Exception("SUPABASE_KEY not found.")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)