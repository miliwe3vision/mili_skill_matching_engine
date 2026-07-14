from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from typing import List
from backend.gemini_services.requirement_extractor import extract_requirements # import this file henil 29/06
from supabase_database.Createsupabase_client import supabase

router = APIRouter()


class TaskModel(BaseModel):
    task_name: str
    description: str

    technologies: List[str]
    tools_and_ide: List[str]
  # remove the requried_experience , estimated hour ,duration day ,req_skill from here - henil 29/06/26
    starting_date: date
    deadline: date


@router.post("/task")
def create_task(task: TaskModel):
    
    # task data into dict henil 29/06/2026 start
    # Convert request data to dictionary
    task_data = task.model_dump()

    # Extract skills and duration
    extracted_data = extract_requirements(task_data)
    #  henil 29/06/2026 end

    data = {
        "task_name": task.task_name,
        "description": task.description,
        "technologies": task.technologies,
        "tools_and_ide": task.tools_and_ide,
        "required_skills": extracted_data["required_skills"],
       # remove the requried_experience , estimated hour from here - henil 29/06/26
        "duration_days": extracted_data["duration_days"],
        "starting_date": str(task.starting_date),
        "deadline": str(task.deadline)
    }

    result = supabase.table("tasks").insert(data).execute()

    return {
        "message": "Task Created Successfully",
        "data": result.data
    }
