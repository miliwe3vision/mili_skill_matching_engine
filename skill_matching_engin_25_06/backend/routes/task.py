from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from typing import List

from supabase_database.Createsupabase_client import supabase

router = APIRouter()


class TaskModel(BaseModel):
    task_name: str
    description: str

    technologies: List[str]
    tools_and_ide: List[str]
    required_skills: List[str]

    required_experience: int
    estimated_hours: int
    duration_days: int

    starting_date: date
    deadline: date


@router.post("/task")
def create_task(task: TaskModel):

    data = {
        "task_name": task.task_name,
        "description": task.description,
        "technologies": task.technologies,
        "tools_and_ide": task.tools_and_ide,
        "required_skills": task.required_skills,
        "required_experience": task.required_experience,
        "estimated_hours": task.estimated_hours,
        "duration_days": task.duration_days,
        "starting_date": str(task.starting_date),
        "deadline": str(task.deadline)
    }

    result = supabase.table("tasks").insert(data).execute()

    return {
        "message": "Task Created Successfully",
        "data": result.data
    }