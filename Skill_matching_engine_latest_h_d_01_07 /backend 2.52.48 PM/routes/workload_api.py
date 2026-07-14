from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.resource_workload.workload_cal import calculate_employee_scores
from supabase_database.Createsupabase_client import supabase

router = APIRouter(
    prefix="/workload",
    tags=["Workload"]
)


# =====================================
# Request Model
# =====================================

class WorkloadRequest(BaseModel):
    emp_id: int



# =====================================
# Calculate Workload
# =====================================

@router.post("/calculate")
def calculate_workload(request: WorkloadRequest):

    try:

        # =====================================
        # Fetch latest assigned task
        # =====================================

        match = (
            supabase
            .table("employee_task_match")
            .select("task_id, similarity_score")
            .eq("emp_id", request.emp_id)
            .order("created_at", desc=True)
            .limit(1)
            .single()
            .execute()
        )

        task_id = match.data["task_id"]
        similarity_score = float(match.data["similarity_score"])

        # Fetch task dates
        task = (
            supabase
            .table("tasks")
            .select("starting_date, deadline")
            .eq("id", task_id)
            .single()
            .execute()
        )

        starting_date = task.data["starting_date"]
        deadline = task.data["deadline"]

        # =====================================
        # Calculate workload
        # =====================================

        result = calculate_employee_scores(
            deadline,
            similarity_score
        )

        # =====================================
        # Prepare workload data
        # =====================================

        workload_data = {
        "emp_id": request.emp_id,
        "task_id": task_id,

        "starting_date": starting_date,
        "deadline": deadline,

        "similarity_score": similarity_score,

        "total_days": result["total_days"],
        "total_task_hours": result["total_task_hours"],
        "total_weekly_available_hours": result["total_weekly_available_hours"],
        "free_hour_before_deadline": result["free_hour_before_deadline"],

        "availability_score": result["availability_score"],
        "active_tasks": result["active_tasks"],
        "task_load": result["task_load"],
        "hours_utilization": result["hours_utilization"],
        "workload_score": result["workload_score"],

        "resource_balancing_score": result["resource_balancing_score"],
        "final_workload_score": result["final_workload_score"]
    }
#supabase.table("employee_workload").insert(workload_data).execute()

        # =====================================
        # Store in database
        # =====================================

        response = (
            supabase
            .table("employee_workload")
            .insert(workload_data)
            .execute()
        )

        return {
            "message": "Employee workload stored successfully",
            "data": response.data
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )