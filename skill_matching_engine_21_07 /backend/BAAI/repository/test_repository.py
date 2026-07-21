from backend.BAAI.repository.employee_repository import fetch_employee_dataset
from backend.BAAI.repository.task_repository import fetch_task_dataset
from backend.BAAI.repository.training_repository import build_training_dataset


print("\nEmployees\n")

print(fetch_employee_dataset())

print("\nTasks\n")

print(fetch_task_dataset())

print("\nTraining Dataset\n")

print(build_training_dataset())