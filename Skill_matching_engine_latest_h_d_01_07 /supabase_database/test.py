
from Createsupabase_client import supabase

response = supabase.table(
    "employee_profiles"
).select("*").execute()

print(response.data)