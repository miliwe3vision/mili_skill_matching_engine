from backend.ai_engine.models.employee_embeddings import generate_employee_embeddings
from backend.ai_engine.models.task_embeddings import generate_task_embeddings

from backend.ai_engine.services.vector_fetch_service import (
    get_employee_vectors,
    get_task_vectors
)

from backend.ai_engine.services.recommendation_service import (
    generate_recommendations
)

from backend.ai_engine.services.recommendation_storage_service import (
    save_recommendations
)

from backend.resource_workload.workload_service import (
    generate_employee_workload
)

from backend.ai_engine.services.task_assignment_service import (
    assign_tasks
)

from backend.ai_engine.services.assignment_storage_service import (
    save_assignments
)


# =====================================================
# Step 1 : Generate Employee Embeddings
# =====================================================

generate_employee_embeddings()

# =====================================================
# Step 2 : Generate Task Embeddings
# =====================================================

generate_task_embeddings()

# =====================================================
# Step 3 : Fetch Stored Vectors
# =====================================================

employee_vectors = get_employee_vectors()
task_vectors = get_task_vectors()

# -----------------------------------------------------
# DEBUG
# Uncomment if you want vector statistics.
# -----------------------------------------------------

# print()
# print("=" * 70)
# print("FETCHING STORED VECTORS")
# print("=" * 70)
# print(f"Employee Vectors : {len(employee_vectors)}")
# print(f"Task Vectors     : {len(task_vectors)}")


# =====================================================
# Step 4 : Generate Similarity Matrix
# =====================================================

recommendations = generate_recommendations(
    employee_vectors,
    task_vectors
)

# -----------------------------------------------------
# DEBUG
# Uncomment to view recommendation statistics.
# -----------------------------------------------------

# print()
# print("=" * 70)
# print("CALCULATING COSINE SIMILARITY")
# print("=" * 70)
# print(f"Recommendations Generated : {len(recommendations)}")


save_recommendations(recommendations)

print()
print("=" * 70)
print("RECOMMENDATIONS STORED SUCCESSFULLY")
print("=" * 70)


# =====================================================
# Step 5 : Generate Employee Workload
# =====================================================

# success_count = 0
# failed_count = 0

# for recommendation in recommendations:

  #  try:

        # -------------------------------------------------
        # DEBUG
        # Uncomment to see workload generation.
        # -------------------------------------------------

        # print(
        #     f"Employee {recommendation['emp_id']} "
        #     f"-> {recommendation['task_name']}"
        # )

        #generate_employee_workload(
        #    recommendation["emp_id"]
       # )

       # success_count += 1

        # print(
        #     f"✓ Employee {recommendation['emp_id']}"
        # )

    #except Exception as e:

      #  failed_count += 1

        # -------------------------------------------------
        # DEBUG
        # Uncomment to view failures.
        # -------------------------------------------------

        # print(
        #     f"✗ Employee {recommendation['emp_id']}"
        # )
        # print(e)


print()
print("=" * 70)
print("AI PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 70)


# =====================================================
# Step 6 : Assign Tasks
# =====================================================

assignments = assign_tasks()

save_assignments(assignments)

# -----------------------------------------------------
# DEBUG
# Uncomment to view final assignments.
# -----------------------------------------------------

# print()
# print("=" * 70)
# print("FINAL TASK ASSIGNMENTS")
# print("=" * 70)
#
# for assignment in assignments:
#
#     print(
#         f"{assignment['employee_name']} "
#         f"-> {assignment['task_name']} "
#         f"(Final Score : {assignment['final_score']})"
#     )
#
# print()
# print("=" * 70)
# print(f"Assigned Tasks : {len(assignments)}")
# print("=" * 70)


print()
print("=" * 70)
print("TASK ASSIGNMENT COMPLETED")
print("=" * 70)