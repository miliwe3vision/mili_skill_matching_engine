import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Path to supabase_database/.env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(BASE_DIR)
)

ENV_PATH = os.path.join(
    PROJECT_ROOT,
    "supabase_database",
    ".env"
)

# Load .env
load_dotenv(ENV_PATH)

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Gemini Model
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def get_required_skills(
    task_name: str,
    description: str
):
    """
    Get required skills from Gemini.
    """

    prompt = f"""
You are an expert software project manager.

Your job is to extract ONLY the essential skills that are directly required to complete the task.

Task Name:
{task_name}

Description:
{description}

Rules:

1. Return ONLY valid JSON.

2. Output format:

{{
    "required_skills": [
        "skill1",
        "skill2"
    ]
}}

3. Extract ONLY the mandatory technical skills.

4. Do NOT include:
- Nice-to-have skills
- Related concepts
- Best practices
- General software engineering knowledge
- Soft skills
- Broad domains
- Future learning topics

5. Return a maximum of 5 skills.

6. If a technology is explicitly mentioned, include it.

7. If the task clearly implies one core development skill, include only that skill.

Examples:

Task:
Create Login API using FastAPI and JWT

Output:
{{
    "required_skills":[
        "FastAPI",
        "JWT",
        "REST API"
    ]
}}

Task:
Build dashboard using Tableau and Power BI

Output:
{{
    "required_skills":[
        "Tableau",
        "Power BI",
        "Dashboard Development"
    ]
}}

Task:
Build CRUD application using Django

Output:
{{
    "required_skills":[
        "Django",
        "CRUD"
    ]
}}

Return ONLY JSON.
Do not explain.
Do not use markdown.
"""

    try:
        response = model.generate_content(prompt)

        result = response.text.strip()

        result = result.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        )

        data = json.loads(result)

        if not isinstance(data, dict):
            return {
                "required_skills": []
            }

        return data

    except Exception:
        return {
            "required_skills": []
        }