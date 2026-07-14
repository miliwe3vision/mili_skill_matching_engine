from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from supabase_database.Createsupabase_client import supabase

router = APIRouter()


# ==========================
# Employee Model
# ==========================

class EmployeeModel(BaseModel):

    user_id: str          # UUID from signup table
    emp_id: int           # Integer from signup table

    name: str
    email: str
    role: str
    experience_years: int

    programming_languages: List[str]
    programming_ratings: List[int]

    frameworks: List[str]
    framework_ratings: List[int]

    tools_and_ide: List[str]
    tools_and_ide_ratings: List[int]


# ==========================
# Add Employee Profile & Skills
# ==========================

@router.post("/employee")
def add_employee(employee: EmployeeModel):

    try:

        # 🔥 STEP 1: GET emp_id FROM signup TABLE
        signup_user = (
            supabase.table("signup")
            .select("emp_id")
            .eq("id", employee.user_id)
            .single()
            .execute()
        )

        emp_id = signup_user.data["emp_id"]

        # 🔥 STEP 2: INSERT PROFILE
        supabase.table("employee_profiles").insert({
            "emp_id": emp_id,
            "name": employee.name,
            "email": employee.email,
            "role": employee.role,
            "experience_years": employee.experience_years
        }).execute()

        # 🔥 STEP 3: INSERT SKILLS
        supabase.table("employee_skills").insert({
            "emp_id": emp_id,
            "programming_languages": employee.programming_languages,
            "programming_ratings": employee.programming_ratings,
            "frameworks": employee.frameworks,
            "framework_ratings": employee.framework_ratings,
            "tools_and_ide": employee.tools_and_ide,
            "tools_and_ide_ratings": employee.tools_and_ide_ratings
        }).execute()

        return {"message": "Employee saved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))