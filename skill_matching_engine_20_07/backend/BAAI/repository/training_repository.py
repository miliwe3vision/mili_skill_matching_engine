import pandas as pd
from backend.BAAI.repository.employee_repository import (
    fetch_employee_dataset
)

from backend.BAAI.repository.task_repository import (
    fetch_task_dataset
)


def build_training_dataset():

    employees = fetch_employee_dataset()

    tasks = fetch_task_dataset()

    pairs = []

    for _, emp in employees.iterrows():

        for _, task in tasks.iterrows():

            pairs.append({

                "employee_text": emp["text"],

                "task_text": task["text"],

                "label": 1

            })

    return pd.DataFrame(pairs)


if __name__ == "__main__":

    df = build_training_dataset()

    print(df.head())

    print()

    print("Total Training Pairs:", len(df))