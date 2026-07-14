from fastapi import APIRouter
from assignment_engine.assign_task import AssignmentDecisionEngine

router = APIRouter(
    prefix="/assignment",
    tags=["Assignment Decision Engine"]
)

engine = AssignmentDecisionEngine()


@router.post("/assign-task")
def assign_task():

    # Sample Task
    task = {
        "task_id": 101,
        "estimated_hours": 20
    }

    # Sample Employee Data
    candidates = [
        {
            "employee_id": 1,
            "name": "Rahul",
            "skill_match": 91,
            "resource_score": 88,
            "available_hours": 30,
            "active_tasks": 2,
            "on_leave": False
        },
        {
            "employee_id": 2,
            "name": "Amit",
            "skill_match": 95,
            "resource_score": 60,
            "available_hours": 5,
            "active_tasks": 3,
            "on_leave": False
        },
        {
            "employee_id": 3,
            "name": "Riya",
            "skill_match": 90,
            "resource_score": 94,
            "available_hours": 40,
            "active_tasks": 1,
            "on_leave": False
        }
    ]

    result = engine.assign_employee(task, candidates)

    return result