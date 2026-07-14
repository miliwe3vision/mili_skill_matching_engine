from database.supabase_client import supabase


def save_assignments(assignments):

    if not assignments:
        print("\nNo task assignments generated.")
        return

    # ----------------------------------------
    # Remove previous assignments
    # ----------------------------------------

    (
        supabase
        .table("task_assignment")
        .delete()
        .neq("emp_id", 0)
        .execute()
    )

    # ----------------------------------------
    # Store New Assignments
    # ----------------------------------------

    (
        supabase
        .table("task_assignment")
        .insert(assignments)
        .execute()
    )

    print("\n" + "=" * 70)
    print("FINAL TASK ASSIGNMENTS")
    print("=" * 70)

    for assignment in assignments:

        print(
            f"✓ {assignment['employee_name']}  →  {assignment['task_name']} "
            f"(Final Score : {assignment['final_score']})"
        )

    print("\n" + "=" * 70)
    print(f"Assigned Tasks : {len(assignments)}")
    print("=" * 70)