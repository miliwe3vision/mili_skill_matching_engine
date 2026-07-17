from datetime import datetime
import math
import os
from supabase import create_client, Client


# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or Key not found in environment variables.")


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


WORKING_HOURS_PER_WEEK = 48
WORKING_HOURS_PER_DAY = 8
WORKING_DAYS_PER_WEEK = 6
MAXIMUM_ACTIVE_TASKS = 10



# -----------------------------
# TOTAL WEEKLY HOURS
# -----------------------------
def calculate_total_weekly_hours(starting_date, deadline_date):
    
    total_days = (deadline_date - starting_date).days + 1

    weeks = math.ceil(
        total_days / WORKING_DAYS_PER_WEEK
    )

    return weeks * WORKING_HOURS_PER_WEEK

#....................add this time...............start.......................
# -----------------------------
# FETCH ACTIVE TASKS
# -----------------------------
def fetch_employee_active_tasks(emp_id):

    try:

        assignments = (
            supabase
            .table("task_assignment")
            .select("task_id")
            .eq("emp_id", emp_id)
            .execute()
        ).data

        active_tasks = []

        for assignment in assignments:

            task = (
                supabase
                .table("tasks")
                .select(
                    "id, starting_date, deadline, status"
                )
                .eq("id", assignment["task_id"])
                .single()
                .execute()
            ).data

            if not task:
                continue

            if task["status"] == "Completed":
                continue

            active_tasks.append(task)

        print(f"Employee {emp_id}")
        print(f"Active Tasks = {len(active_tasks)}")

        return active_tasks

    except Exception as e:

        print("fetch_employee_active_tasks ERROR:", e)

        return []
    
# -----------------------------
# CALCULATE EXISTING WORKLOAD
# -----------------------------
def calculate_existing_workload(existing_tasks):

    total_hours = 0

    starts = []

    deadlines = []

    for task in existing_tasks:

        start = datetime.strptime(
            task["starting_date"],
            "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            task["deadline"],
            "%Y-%m-%d"
        ).date()

        days = (end - start).days + 1

        total_hours += days * WORKING_HOURS_PER_DAY

        starts.append(start)

        deadlines.append(end)

    return {

        "total_hours": total_hours,

        "starts": starts,

        "deadlines": deadlines

    }
# -----------------------------
# CALCULATE AVAILABLE HOURS
# -----------------------------
def calculate_available_hours(

    existing_work,

    new_start,

    new_deadline

):

    starts = existing_work["starts"] + [new_start]

    deadlines = existing_work["deadlines"] + [new_deadline]

    earliest = min(starts)

    latest = max(deadlines)

    total_days = (latest - earliest).days + 1

    weeks = math.ceil(
        total_days /
        WORKING_DAYS_PER_WEEK
    )

    return weeks * WORKING_HOURS_PER_WEEK
#..........add this time.........................end............................
# -----------------------------
# EXISTING TASK HOURS
# -----------------------------
def calculate_existing_task_hours(tasks):

    total_hours = 0
    total_days = 0

    for task in tasks:

        start = datetime.strptime(
            task["starting_date"],
            "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            task["deadline"],
            "%Y-%m-%d"
        ).date()

        days = (end - start).days + 1

        total_days += days
        total_hours += days * WORKING_HOURS_PER_DAY

    return {

        "total_days": total_days,
        "total_hours": total_hours

    }

# -----------------------------
# FETCH TASK COMPLEXITY & PRIORITY
# -----------------------------
def get_task_details(task_id):

    try:

        response = (
            supabase
            .table("tasks")
            .select(
                "complexity, priority"
            )
            .eq("id", task_id)
            .single()
            .execute()
        )

        return response.data or {}


    except Exception as e:

        print(
            f"Task details error: {e}"
        )

        return {}



# -----------------------------
# COMPLEXITY SCORE
# -----------------------------
def calculate_complexity_score(complexity):

    if not complexity:
        return 50


    complexity = complexity.lower()


    score_mapping = {

        "low": 30,

        "medium": 60,

        "high": 85,

        "very high": 100

    }


    return score_mapping.get(
        complexity,
        50
    )



# -----------------------------
# PRIORITY SCORE
# -----------------------------
def calculate_priority_score(priority):

    if not priority:
        return 50


    priority = priority.lower()


    score_mapping = {

        "low": 30,

        "medium": 60,

        "high": 80,

        "critical": 100

    }


    return score_mapping.get(
        priority,
        50
    )



# -----------------------------
# AVAILABILITY
# -----------------------------
def calculate_availability(total_weekly_hours):

    free_hours = total_weekly_hours

    availability_score = 100


    return {

        "availability_score": round(
            availability_score,
            2
        ),

        "free_hours": free_hours,

        "weekly_hours": total_weekly_hours
    }




# -----------------------------
# WORKLOAD SCORE
# -----------------------------
# def calculate_workload(
#         total_days,
#         total_weekly_hours,
#         active_tasks,
#         complexity_score,
#         priority_score
# ):


#     total_task_hours = (
#         total_days *
#         WORKING_HOURS_PER_DAY
#     )


#     task_load_score = (
#         active_tasks /
#         MAXIMUM_ACTIVE_TASKS
#     ) * 100



#     hours_utilization = min(
#         (
#             total_task_hours /
#             total_weekly_hours
#         ) * 100,

#         100
#     )


#     # Final workload calculation
#     workload_score = (

#         task_load_score * 0.25

#         +

#         hours_utilization * 0.45

#         +

#         complexity_score * 0.20

#         +

#         priority_score * 0.10

#     )


#     return {

#         "workload_score": round(
#             workload_score,
#             2
#         ),

#         "hours_utilization": round(
#             hours_utilization,
#             2
#         ),

#         "task_load_score": round(
#             task_load_score,
#             2
#         ),

#         "complexity_score": complexity_score,

#         "priority_score": priority_score
#     }
# new calculation by mili 17/07/26------start------

def calculate_workload(

        total_task_hours,

        available_hours,

        active_tasks,

        complexity_score,

        priority_score

):

    task_load_score = (

        active_tasks /
        MAXIMUM_ACTIVE_TASKS

    ) * 100

    hours_utilization = min(

        (

            total_task_hours /
            available_hours

        ) * 100,

        100

    )

    workload_score = (

        task_load_score * 0.25

        +

        hours_utilization * 0.45

        +

        complexity_score * 0.20

        +

        priority_score * 0.10

    )

    return {

        "workload_score": round(workload_score, 2),

        "hours_utilization": round(hours_utilization, 2),

        "task_load_score": round(task_load_score, 2),

        "complexity_score": complexity_score,

        "priority_score": priority_score

    }
# new calculation by mili 17/07/26------end-------
# -----------------------------
# RESOURCE BALANCE
# -----------------------------
def calculate_resource_balance(
        availability_score,
        workload_score
):

    remaining_capacity = (
        100 - workload_score
    )


    resource_balancing_score = (

        availability_score * 0.5
        +
        remaining_capacity * 0.50

    )

    return round(
        resource_balancing_score,
        2
    )
# -----------------------------
# FINAL PIPELINE
# -----------------------------
# def calculate_employee_scores(
#         starting_date,
#         deadline,
#         skill_matching_score,
#         emp_id,
#         task_id
# ):
def calculate_employee_scores(

        starting_date,

        deadline,

        skill_matching_score,

        emp_id,

        task_id,

        active_tasks

):

    starting_date = datetime.strptime(
        starting_date,
        "%Y-%m-%d"
    ).date()

    deadline_date = datetime.strptime(
        deadline,
        "%Y-%m-%d"
    ).date()

    if deadline_date <= starting_date:

        raise ValueError(
            "Deadline must be greater than Starting Date."
        )

    total_days = (
        deadline_date -
        starting_date
    ).days + 1

    # total_weekly_hours = calculate_total_weekly_hours(
    #     starting_date,
    #     deadline_date
    # )

    # -----------------------------
    # TASK COMPLEXITY + PRIORITY
    # -----------------------------

    task_details = get_task_details(
        task_id
    )

    complexity_score = calculate_complexity_score(
        task_details.get(
            "complexity"
        )
    )

    priority_score = calculate_priority_score(
        task_details.get(
            "priority"
        )
    )
    # -----------------------------
    # ACTIVE TASKS
    # -----------------------------

    # active_tasks = fetch_employee_active_tasks(
    #     emp_id
    # )

    # active_tasks += 1
   # add mili ---------17/07/26---------start--- 
    # existing_tasks = fetch_employee_active_tasks(emp_id)

    # active_tasks = 1+ len(existing_tasks) 
    
    # existing_work = calculate_existing_workload(
    # existing_tasks
    # )
    existing_tasks = fetch_employee_active_tasks(
    emp_id
    )

    existing_work = calculate_existing_workload(
        existing_tasks
    )

    new_task_hours = (
    total_days *
    WORKING_HOURS_PER_DAY
    )

    grand_total_hours = (
    existing_work["total_hours"] +
    new_task_hours
    )

    available_hours = calculate_available_hours(

    existing_work,

    starting_date,

    deadline_date

    )

    # availability = calculate_availability(
    #     total_weekly_hours
    # )
    
    availability = calculate_availability(
    available_hours
    )

    # workload = calculate_workload(

    #     total_days,

    #     total_weekly_hours,

    #     active_tasks,

    #     complexity_score,

    #     priority_score

    # )
    
    workload = calculate_workload(

    grand_total_hours,

    available_hours,

    active_tasks,

    complexity_score,

    priority_score

    )
    # add mili ---------17/07/26---------end--- 
        
    resource_score = calculate_resource_balance(

        availability["availability_score"],

        workload["workload_score"]

    )

    # -----------------------------
    # SKILL SCORE NORMALIZATION
    # -----------------------------

    if skill_matching_score <= 1:

        skill_matching_score *= 100
    # -----------------------------
    # FINAL SCORE
    # -----------------------------

    final_workload_score = (

        skill_matching_score * 0.70
        +
        resource_score * 0.30

    )

    return {


        "deadline": deadline,
        "total_days": total_days,

        # "total_task_hours":
        #     total_days *
        #     WORKING_HOURS_PER_DAY,
        
        "total_task_hours":
            grand_total_hours,

        # "total_weekly_available_hours":
        #     total_weekly_hours,
        
        "total_weekly_available_hours":
            available_hours,
            
        "free_hour_before_deadline":
            availability["free_hours"],

        "availability_score":
            availability["availability_score"],

        "active_tasks":
            active_tasks,

        "task_load":
            workload["task_load_score"],

        "hours_utilization":
            workload["hours_utilization"],

        "complexity_score":
            workload["complexity_score"],

        "priority_score":
            workload["priority_score"],

        "workload_score":
            workload["workload_score"],

        "resource_balancing_score":
            resource_score,

        "skill_matching_score":
            round(
                skill_matching_score,
                2
            ),
        "final_workload_score":
            round(
                final_workload_score,
                2
            )
            
    }
    
# -----------------------------
# EXISTING TASK HOURS
# -----------------------------
def calculate_existing_task_hours(tasks):

    total_hours = 0
    total_days = 0

    for task in tasks:

        start = datetime.strptime(
            task["starting_date"],
            "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            task["deadline"],
            "%Y-%m-%d"
        ).date()

        days = (end - start).days + 1

        total_days += days
        total_hours += days * WORKING_HOURS_PER_DAY

    return {

        "total_days": total_days,
        "total_hours": total_hours

    }
    
# -----------------------------
# AVAILABLE HOURS WINDOW
# -----------------------------
def calculate_employee_available_hours(
        existing_tasks,
        new_start,
        new_deadline
):

    starts = [new_start]
    ends = [new_deadline]

    for task in existing_tasks:

        starts.append(
            datetime.strptime(
                task["starting_date"],
                "%Y-%m-%d"
            ).date()
        )

        ends.append(
            datetime.strptime(
                task["deadline"],
                "%Y-%m-%d"
            ).date()
        )

    earliest = min(starts)
    latest = max(ends)

    total_days = (
        latest - earliest
    ).days + 1

    weeks = math.ceil(
        total_days /
        WORKING_DAYS_PER_WEEK
    )

    return weeks * WORKING_HOURS_PER_WEEK