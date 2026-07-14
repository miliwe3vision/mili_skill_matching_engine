from backend.ai_engine.database.supabase_client import supabase


def assign_tasks():

    # ----------------------------------------
    # Fetch Similarity Matrix
    # ----------------------------------------

    matches = (
        supabase
        .table("employee_task_match")
        .select("*")
        .execute()
    ).data

    # ----------------------------------------
    # Fetch Employee Workload
    # ----------------------------------------

    workloads = (
        supabase
        .table("employee_workload")
        .select("emp_id, final_workload_score")
        .execute()
    ).data

    workload_map = {
        row["emp_id"]: float(row["final_workload_score"])
        for row in workloads
    }

    # ----------------------------------------
    # Build Candidate List
    # ----------------------------------------

    candidates = []

    for row in matches:

        similarity = float(row["similarity_score"])

        workload = workload_map.get(
            row["emp_id"],
            0
        )

        final_score = (
            similarity * 0.70 +
            workload * 0.30
        )

        candidates.append({

            "emp_id": row["emp_id"],

            "employee_name": row["name"],

            "task_id": row["task_id"],

            "task_name": row["task_name"],

            "similarity_score": similarity,

            "workload_score": workload,

            "final_score": round(final_score, 2)

        })

    # ----------------------------------------
    # Highest Final Score First
    # ----------------------------------------

    candidates.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    assigned_employees = set()
    assigned_tasks = set()

    final_assignments = []

    # ----------------------------------------
    # One Employee -> One Task
    # One Task -> One Employee
    # ----------------------------------------

    for row in candidates:

        if row["emp_id"] in assigned_employees:
            continue

        if row["task_id"] in assigned_tasks:
            continue

        final_assignments.append(row)

        assigned_employees.add(row["emp_id"])
        assigned_tasks.add(row["task_id"])

    return final_assignments