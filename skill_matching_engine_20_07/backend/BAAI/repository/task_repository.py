import pandas as pd

from database.supabase_client import supabase


def fetch_task_dataset():

    response = (

        supabase

        .table("tasks")

        .select("*")

        .execute()

    )

    tasks = response.data

    dataset = []

    for task in tasks:

        text = " ".join(

            (task.get("technologies") or [])

            +

            (task.get("tools_and_ide") or [])

        )

        dataset.append({

            "task_id": task["id"],

            "text": text

        })

    df = pd.DataFrame(dataset)

    return df


if __name__ == "__main__":

    df = fetch_task_dataset()

    print(df.head())