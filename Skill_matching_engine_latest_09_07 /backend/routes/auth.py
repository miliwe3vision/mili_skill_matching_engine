from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.supabase_client import supabase

router = APIRouter()


# ==========================
# Signup Model
# ==========================

class SignupModel(BaseModel):
    username: str
    email: str
    password: str
    role: str = "employee"


# ==========================
# Login Model
# ==========================

class LoginModel(BaseModel):
    email: str
    password: str


# ==========================
# Signup API
# ==========================

@router.post("/signup")
def signup(user: SignupModel):

    try:

        response = (
            supabase.table("signup")
            .insert({
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "role": user.role
            })
            .execute()
        )

        return {
            "message": "Signup successful",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ==========================
# Login API
# ==========================

@router.post("/login")
def login(user: LoginModel):

    try:

        response = (
            supabase.table("signup")
            .select("*")
            .eq("email", user.email)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        db_user = response.data[0]

        if db_user["password"] != user.password:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        return {
            "message": "Login successful",
            "user": {
                "id": db_user["id"],
                "emp_id": db_user["emp_id"],          # Auto-generated Employee ID
                "username": db_user["username"],
                "email": db_user["email"],
                "role": db_user["role"],
                "skills_completed": db_user["skills_completed"]
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# =====================================
# mili GET LOGGED-IN USER DETAILS
# =====================================

@router.get("/user/{user_id}")
def get_user(user_id: str):

    result = (
        supabase
        .table("signup")
        .select("username, role")
        .eq("id", user_id)
        .single()
        .execute()
    )

    return result.data

