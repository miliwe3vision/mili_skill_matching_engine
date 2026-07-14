from ai_engine.models.employee_embeddings import generate_employee_embeddings
from ai_engine.models.task_embeddings import generate_task_embeddings


print("\n")
print("=" * 70)
print("AI VECTOR GENERATION ENGINE")
print("=" * 70)

generate_employee_embeddings()

generate_task_embeddings()

print("\n")
print("=" * 70)
print("ALL VECTORS STORED SUCCESSFULLY")
print("=" * 70)