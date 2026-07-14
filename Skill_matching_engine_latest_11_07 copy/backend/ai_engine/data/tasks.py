from database.supabase_client import supabase

# --------------------------------------------------------
# Fetch ONLY Pending Tasks
# --------------------------------------------------------

response = (
    supabase
    .table("tasks")
    .select("*")
    .eq("status", "Pending")      # <-- Only pending tasks
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

        "required_skills": row.get("required_skills") or [],

        "status": row.get("status")   # optional
    }

    tasks.append(task)