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

    # ====================================================
    # OLD LOGIC (COMMENTED)
    # ----------------------------------------------------
    # Previously workload was generated before assignment
    # and stored for every Employee × Task combination.
    #
    # workloads = (
    #     supabase
    #     .table("employee_workload")
    #     .select("emp_id, final_workload_score")
    #     .execute()
    # ).data
    #
    # workload_map = {
    #     row["emp_id"]: float(row["final_workload_score"])
    #     for row in workloads
    # }
    # ====================================================

    # ----------------------------------------
    # Build Candidate List
    # ----------------------------------------

    candidates = []

    for row in matches:

        similarity = float(row["similarity_score"])

        # ====================================================
        # NEW LOGIC
        #
        # Since workload is now generated AFTER assignment,
        # only similarity is used during candidate ranking.
        #
        # Workload will be calculated once the final
        # employee-task pair is selected.
        # ====================================================

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

        # ====================================================
        # Generate workload ONLY for selected assignment
        # ====================================================

        workload_data = generate_employee_workload(

            emp_id=row["emp_id"],

            task_id=row["task_id"],

            similarity_score=row["similarity_score"]

        )

        # Update candidate with calculated workload

        row["workload_score"] = workload_data["workload_score"]

        row["final_score"] = workload_data["final_workload_score"]

        final_assignments.append(row)

        assigned_employees.add(row["emp_id"])

        assigned_tasks.add(row["task_id"])

    return final_assignments