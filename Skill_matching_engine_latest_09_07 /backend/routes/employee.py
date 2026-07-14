print("EMPLOYEE FILE LOADED")  # Drashti 27/06/2026
from backend.services.feature_pipeline import process_employee

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from database.supabase_client import supabase

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
        # GET USER DETAILS FROM SIGNUP TABLE
        # =====================================

        signup_user = (
            supabase
            .table("signup")
            .select("emp_id, username, email")
            .eq("id", employee.user_id)
            .single()
            .execute()
        )

        if not signup_user.data:
            raise HTTPException(
                status_code=404,
                detail="Employee not found."
            )

        db_user = signup_user.data

        # =====================================
        # VALIDATE EMPLOYEE DETAILS
        # =====================================

        if employee.emp_id != db_user["emp_id"]:
            raise HTTPException(
                status_code=400,
                detail="Employee ID does not match the signup record."
            )

        if employee.name.strip() != db_user["username"].strip():
            raise HTTPException(
                status_code=400,
                detail="Employee name does not match the signup record."
            )

        if employee.email.strip().lower() != db_user["email"].strip().lower():
            raise HTTPException(
                status_code=400,
                detail="Employee email does not match the signup record."
            )

        # =====================================
        # TASK 4 FEATURE ENGINEERING PIPELINE
        # =====================================

        result = process_employee({

            "emp_id": db_user["emp_id"],

            "name": db_user["username"],
            "email": db_user["email"],
            "role": employee.role,

            "experience": employee.experience_years,

            "languages": employee.programming_languages,
            "frameworks": employee.frameworks,
            "tools": employee.tools_and_ide,

            "programming_ratings": employee.programming_ratings,
            "framework_ratings": employee.framework_ratings,
            "tools_and_ide_ratings": employee.tools_and_ide_ratings
        })

        # =====================================
        # UPDATE signup TABLE
        # skills_completed = TRUE
        # =====================================

        supabase.table("signup").update(
            {
                "skills_completed": True
            }
        ).eq(
            "id",
            employee.user_id
        ).execute()

        return {
            "message": "Employee processed successfully",
            "result": result
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================
# GET ALL EMPLOYEES
# =====================================

@router.get("/employees")
def get_all_employees():

    result = (
        supabase
        .table("employee_profiles")
        .select("emp_id,name,email,role,experience_years")
        .order("emp_id")
        .execute()
    )

    return result.data