from google import genai
from dotenv import load_dotenv
import os
import json
import time

load_dotenv("../supabase_database/.env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MAX_RETRIES = 3


def fallback_validation(skills):
    """
    Fallback used when Gemini is unavailable.
    Keeps the application running.
    """

    known_languages = {
        "python", "java", "c", "c++", "c#", "javascript",
        "typescript", "php", "go", "rust", "kotlin", "swift"
    }

    known_frameworks = {
        "django", "flask", "fastapi", "react", "angular",
        "vue", "spring", "spring boot",
        "langgraph", "llamaindex"
    }

    known_tools = {
        "git", "github", "docker", "postman", "mysql",
        "mongodb", "supabase", "colab", "vs code",
        "vscode", "aws", "jira"
    }

    result = {
        "languages": [],
        "frameworks": [],
        "tools": [],
        "invalid_skills": []
    }

    for skill in skills:

        s = skill.lower().strip()

        if s in known_languages:
            result["languages"].append(s)

        elif s in known_frameworks:
            result["frameworks"].append(s)

        elif s in known_tools:
            result["tools"].append(s)

        else:
            result["invalid_skills"].append(s)

    return result


def validate_skills(skills):

    print("GEMINI CALLED")

    prompt = f"""
You are a strict software technology validation engine.

Classify each skill into exactly one category.

Return ONLY JSON.

Schema:

{{
    "languages": [],
    "frameworks": [],
    "tools": [],
    "invalid_skills": []
}}

Skills:
{skills}
"""

    delay = 2

    for attempt in range(MAX_RETRIES):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            text = response.text.strip()

            text = text.replace("```json", "")
            text = text.replace("```", "")

            return json.loads(text)

        except Exception as e:

            print(f"Gemini attempt {attempt + 1} failed:")
            print(e)

            if attempt < MAX_RETRIES - 1:
                time.sleep(delay)
                delay *= 2

    print("Using fallback validation.")

    return fallback_validation(skills)