print("EMPLOYEE FILE LOADED")  # Drashti 27/06/2026
from backend.services.feature_pipeline import process_employee # Drashti 27/06/2026

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from supabase_database.Createsupabase_client import supabase

router = APIRouter()


# ==========================
# Employee Model
# ==========================

class EmployeeModel(BaseModel):

    user_id: str
    emp_id: int

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
# Add Employee
# ==========================

@router.post("/employee")
def add_employee(employee: EmployeeModel):

    print("EMPLOYEE ROUTE HIT")

    try:

        # =====================================
        # GET emp_id FROM signup
        # =====================================

        signup_user = (
            supabase
            .table("signup")
            .select("emp_id")
            .eq("id", employee.user_id)
            .single()
            .execute()
        )

        emp_id = signup_user.data["emp_id"]

        # =====================================
        # TASK 4 FEATURE ENGINEERING PIPELINE
        # =====================================

        result = process_employee({

            "emp_id": emp_id,

            "name": employee.name,
            "email": employee.email,
            "role": employee.role,

            "experience": employee.experience_years,

            "languages": employee.programming_languages,
            "frameworks": employee.frameworks,
            "tools": employee.tools_and_ide,

            "programming_ratings": employee.programming_ratings,
            "framework_ratings": employee.framework_ratings,
            "tools_and_ide_ratings": employee.tools_and_ide_ratings
        })

        return {
            "message": "Employee processed successfully",
            "result": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
