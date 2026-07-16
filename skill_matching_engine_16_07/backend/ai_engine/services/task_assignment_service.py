from datetime import datetime

from database.supabase_client import supabase

from backend.resource_workload.workload_service import (
    generate_employee_workload,
)


# ==========================================================
# Priority Score
# ==========================================================

def get_priority_score(priority):

    priority_map = {

        "Critical": 100,
        "High": 80,
        "Medium": 60,
        "Low": 40,
        "Very Low": 20

    }

    return priority_map.get(priority, 50)



# ==========================================================
# Complexity Score
# ==========================================================

def get_complexity_score(complexity):

    complexity_map = {

        "Very Easy": 50,
        "Easy": 60,
        "Medium": 75,
        "Hard": 90,
        "Expert": 100

    }

    return complexity_map.get(complexity, 70)



# ==========================================================
# Deadline Urgency Score
# ==========================================================

def get_deadline_score(deadline):

    deadline_date = datetime.strptime(
        deadline,
        "%Y-%m-%d"
    )

    days_left = (
        deadline_date -
        datetime.today()
    ).days


    if days_left <= 2:
        return 100

    elif days_left <= 5:
        return 90

    elif days_left <= 10:
        return 80

    elif days_left <= 15:
        return 70

    elif days_left <= 20:
        return 60

    return 50



# ==========================================================
# Intelligent Task Assignment
# ==========================================================

def assign_tasks():


    # ----------------------------------------
    # Employee Task Similarity
    # ----------------------------------------

    matches = (

        supabase
        .table("employee_task_match")
        .select("*")
        .execute()

    ).data


    if not matches:

        print("No employee matches found.")

        return []



    # ----------------------------------------
    # Pending Tasks
    # ----------------------------------------

    pending_tasks = (

        supabase
        .table("tasks")
        .select("*")
        .eq("status", "Pending")
        .execute()

    ).data



    if not pending_tasks:

        print("No pending tasks.")

        return []



    pending_lookup = {

        task["id"]: task

        for task in pending_tasks

    }



    candidates = []



    # ----------------------------------------
    # Generate Candidates
    # ----------------------------------------

    for row in matches:


        if row["task_id"] not in pending_lookup:

            continue



        task = pending_lookup[row["task_id"]]



        priority_score = get_priority_score(
            task.get("priority")
        )


        complexity_score = get_complexity_score(
            task.get("complexity")
        )


        urgency_score = get_deadline_score(
            task["deadline"]
        )



        candidates.append({


            "emp_id":
                row["emp_id"],


            "employee_name":
                row["name"],


            "task_id":
                row["task_id"],


            "task_name":
                row["task_name"],



            "similarity_score":
                float(row["similarity_score"]),



            # calculated values
            # used only for ranking

            "priority_score":
                priority_score,


            "complexity_score":
                complexity_score,


            "urgency_score":
                urgency_score,



            "priority":
                task["priority"],



            "complexity":
                task["complexity"],



            "deadline":
                task["deadline"],



            "workload_score":
                0,


            "final_score":
                0

        })



    candidates.sort(

        key=lambda x:
            x["similarity_score"],

        reverse=True

    )



    # ----------------------------------------
    # Assignment Process
    # ----------------------------------------

    assigned_tasks = set()

    final_assignments = []



    for row in candidates:



        if row["task_id"] in assigned_tasks:

            continue



        task = (

            supabase
            .table("tasks")
            .select("*")
            .eq("id", row["task_id"])
            .single()
            .execute()

        ).data



        if not task:

            continue



        if task["status"] != "Pending":

            continue



        # ----------------------------------------
        # Workload Calculation
        # ----------------------------------------

        try:


            workload = generate_employee_workload(

                emp_id=row["emp_id"],

                task_id=row["task_id"],

                similarity_score=row["similarity_score"]

            )


        except Exception as e:


            print(
                f"Workload Error ({row['employee_name']}): {e}"
            )

            continue




        row["workload_score"] = round(

            float(
                workload["workload_score"]
            ),

            2

        )




        # ----------------------------------------
        # Final AI Score
        # ----------------------------------------

        final_score = (


            row["similarity_score"] * 0.45


            +

            row["workload_score"] * 0.25


            +

            row["priority_score"] * 0.15


            +

            row["urgency_score"] * 0.10


            +

            row["complexity_score"] * 0.05

        )



        row["final_score"] = round(
            final_score,
            2
        )




        # ----------------------------------------
        # Update Task Status
        # ----------------------------------------

        (

            supabase
            .table("tasks")
            .update({

                "status": "Assigned"

            })
            .eq(
                "id",
                row["task_id"]
            )
            .execute()

        )




        final_assignments.append({


            "emp_id":
                row["emp_id"],


            "employee_name":
                row["employee_name"],


            "task_id":
                row["task_id"],


            "task_name":
                row["task_name"],


            "similarity_score":
                row["similarity_score"],


            "workload_score":
                row["workload_score"],


            "priority":
                row["priority"],


            "complexity":
                row["complexity"],


            "deadline":
                row["deadline"],


            "priority_score":
                row["priority_score"],


            "complexity_score":
                row["complexity_score"],


            "urgency_score":
                row["urgency_score"],


            "final_score":
                row["final_score"]

        })



        assigned_tasks.add(
            row["task_id"]
        )



        print(

            f"✓ {row['employee_name']} "
            f"→ {row['task_name']} "
            f"Final Score : {row['final_score']}"

        )

    final_assignments.sort(

        key=lambda x:
            x["final_score"],

        reverse=True

    )

    print("\n" + "=" * 70)

    print("SMART TASK ASSIGNMENT COMPLETED")

    print("=" * 70)

    print(
        f"Assignments : {len(final_assignments)}"
    )

    print("=" * 70)



    return final_assignments