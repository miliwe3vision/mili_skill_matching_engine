from ai_engine.models.employee_embeddings import generate_employee_embeddings
from ai_engine.models.task_embeddings import generate_task_embeddings

from ai_engine.services.vector_fetch_service import (
    get_employee_vectors,
    get_task_vectors
)

from ai_engine.services.recommendation_service import generate_recommendations

from ai_engine.services.recommendation_storage_service import (
    save_recommendations
)



print()
print("=" * 70)
print("AI SKILL MATCHING ENGINE")
print("=" * 70)

# -------------------------------------------------
# Step 1 : Generate Employee Vectors
# -------------------------------------------------

generate_employee_embeddings()

# -------------------------------------------------
# Step 2 : Generate Task Vectors
# -------------------------------------------------

generate_task_embeddings()

print()
print("=" * 70)
print("FETCHING STORED VECTORS")
print("=" * 70)

employee_vectors = get_employee_vectors()
task_vectors = get_task_vectors()

print(f"Employee Vectors : {len(employee_vectors)}")
print(f"Task Vectors     : {len(task_vectors)}")

print()
print("=" * 70)
print("CALCULATING COSINE SIMILARITY")
print("=" * 70)

recommendations = generate_recommendations(
    employee_vectors,
    task_vectors
)

print(f"Recommendations Generated : {len(recommendations)}")

print()
print("=" * 70)
print("STORING RECOMMENDATIONS")
print("=" * 70)

save_recommendations(recommendations)

print()
print("=" * 70)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 70)

