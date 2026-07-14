from database.supabase_client import supabase

from backend.resource_workload.workload_service import (
    generate_employee_workload
)


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
    # Fetch ONLY Pending Tasks
    # ----------------------------------------

    pending_tasks = (
        supabase
        .table("tasks")
        .select("id")
        .eq("status", "Pending")   # <-- Capital P
        .execute()
    ).data

    pending_task_ids = {
        task["id"]
        for task in pending_tasks
    }

    # ----------------------------------------
    # Build Candidate List
    # ----------------------------------------

    candidates = []

    for row in matches:

        # ----------------------------------------
        # Ignore already assigned/completed tasks
        # ----------------------------------------

        if row["task_id"] not in pending_task_ids:
            continue

        similarity = float(row["similarity_score"])

        workload = 0

        final_score = similarity

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
    # Highest Score First
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

        # ----------------------------------------
        # Double-check task is still Pending
        # ----------------------------------------

        task = (
            supabase
            .table("tasks")
            .select("status")
            .eq("id", row["task_id"])
            .single()
            .execute()
        ).data

        if not task:
            continue

        if task["status"] != "pending":
            continue

        # ----------------------------------------
        # Generate Workload
        # ----------------------------------------

        workload_data = generate_employee_workload(

            emp_id=row["emp_id"],

            task_id=row["task_id"],

            similarity_score=row["similarity_score"]

        )

        row["workload_score"] = workload_data["workload_score"]

        row["final_score"] = workload_data["final_workload_score"]

        final_assignments.append(row)

        # ----------------------------------------
        # FREEZE TASK
        # ----------------------------------------

        (
            supabase
            .table("tasks")
            .update({
                "status": "Assigned"
            })
            .eq("id", row["task_id"])
            .execute()
        )

        assigned_employees.add(row["emp_id"])

        assigned_tasks.add(row["task_id"])

    return final_assignments