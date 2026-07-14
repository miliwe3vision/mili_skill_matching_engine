# Gemini Validator by drashti
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv("../supabase_database/.env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def validate_skills(skills):
    print("GEMINI CALLED")
    prompt = f"""
    You are a strict software technology validation engine.

    Your task is NOT to guess.

    Your task is to validate whether each skill is a REAL and RECOGNIZED software technology.

    Classify every skill into exactly one category:

    1. language
    2. framework
    3. tool
    4. invalid

    Definitions:

    - language:
    A programming language used for software development.
    Examples: python, java, c++, javascript, typescript, go, rust, etc...

    - framework:
    A software framework or development library used to build applications.
    Examples: react, angular, vue, django, flask, fastapi, spring boot, langgraph, llamaindex, etc...

    - tool:
    IDEs, databases, cloud platforms, DevOps tools, testing tools, version control systems, software products.
    Examples: git, github, docker, jira, postman, mysql, mongodb, aws, vscode, etc...

    - invalid:
    Any random text, keyboard mash, typo, personal name, company name, sentence fragment, unknown word, or term that is NOT a recognized software technology.

    CRITICAL RULES:

    - Never guess.
    - Never infer.
    - Never assume.
    - If confidence is below 95%, classify as invalid.
    - Unknown technologies must be invalid.
    - Random keyboard text must be invalid.
    - Typos must be invalid.
    - Made-up words must be invalid.
    - If a term cannot be verified as a real software technology, classify as invalid.

    Examples:

    python -> language
    java -> language
    react -> framework
    fastapi -> framework
    langgraph -> framework
    git -> tool
    docker -> tool
    jira -> tool

    asdf -> invalid
    qwerty -> invalid
    abc123 -> invalid
    hello -> invalid
    testskill -> invalid

    Return ONLY valid JSON.

    Output schema:

    {{
        "languages": [],
        "frameworks": [],
        "tools": [],
        "invalid_skills": []
    }}

    Skills:
    {skills}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown if Gemini adds it
    text = text.replace("```json", "")
    text = text.replace("```", "")

    return json.loads(text)