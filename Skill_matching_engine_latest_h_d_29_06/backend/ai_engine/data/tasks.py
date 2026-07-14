from ai_engine.database.supabase_client import supabase

# --------------------------------------------------------
# Fetch Tasks
# --------------------------------------------------------

response = (
    supabase
    .table("tasks")
    .select("*")
    .execute()
)

tasks = []

for row in response.data:

    task = {

        "id": row["id"],

        "title": row["task_name"],

        "description": row.get("description") or "",

        "technologies": row.get("technologies") or [],

        "tools": row.get("tools_and_ide") or [],

        "required_skills": row.get("required_skills") or []

    }

    tasks.append(task)