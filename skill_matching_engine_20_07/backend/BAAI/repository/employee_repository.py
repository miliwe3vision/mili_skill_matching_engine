import pandas as pd

from database.supabase_client import supabase


def fetch_employee_dataset():

    response = (
        supabase
        .table("employee_skills")
        .select("*")
        .execute()
    )

    employees = response.data

    dataset = []

    for emp in employees:

        text = " ".join(

            (emp.get("programming_languages") or [])

            +

            (emp.get("frameworks") or [])

            +

            (emp.get("tools_and_ide") or [])

        )

        dataset.append({

            "emp_id": emp["emp_id"],

            "text": text

        })

    df = pd.DataFrame(dataset)

    return df


if __name__ == "__main__":

    df = fetch_employee_dataset()

    print(df.head())