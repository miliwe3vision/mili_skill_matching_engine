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


print()
print("=" * 70)
print("AI SKILL MATCHING ENGINE")
print("=" * 70)

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

print()
print("=" * 70)
print("FETCHING STORED VECTORS")
print("=" * 70)

employee_vectors = get_employee_vectors()
task_vectors = get_task_vectors()

print(f"Employee Vectors : {len(employee_vectors)}")
print(f"Task Vectors     : {len(task_vectors)}")

# =====================================================
# Step 4 : Generate Similarity Matrix
# =====================================================

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
print("RECOMMENDATIONS STORED SUCCESSFULLY")
print("=" * 70)

# =====================================================
# Step 5 : Generate Employee Workload
# =====================================================

print()
print("=" * 70)
print("GENERATING EMPLOYEE WORKLOAD")
print("=" * 70)

success_count = 0
failed_count = 0

for recommendation in recommendations:

    try:

        # -----------------------------------------------------
        # DEBUG LOGS
        # Uncomment these lines if you want to see
        # every Employee → Task workload calculation.
        # -----------------------------------------------------

        # print(
        #     f"\nEmployee {recommendation['emp_id']} "
        #     f"-> Task: {recommendation['task_name']}"
        # )

        generate_employee_workload(
            recommendation["emp_id"]
        )

        # print(
        #     f"✓ Workload generated for "
        #     f"Employee {recommendation['emp_id']}"
        # )

        success_count += 1

    except Exception as e:

        # -----------------------------------------------------
        # DEBUG LOGS
        # Uncomment to see workload generation failures.
        # -----------------------------------------------------

        # print(
        #     f"✗ Employee {recommendation['emp_id']} failed"
        # )
        #
        # print(f"Reason : {e}")

        failed_count += 1

print()
print("=" * 70)
print("WORKLOAD GENERATION COMPLETED")
print("=" * 70)

print(f"Successful : {success_count}")
print(f"Failed     : {failed_count}")

# =====================================================
# Step 6 : AI Pipeline Completed
# =====================================================

print()
print("=" * 70)
print("AI PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 70)

# =====================================================
# Step 7 : Assign Tasks
# =====================================================

print()
print("=" * 70)
print("ASSIGNING TASKS")
print("=" * 70)

assignments = assign_tasks()

save_assignments(assignments)

# -----------------------------------------------------
# DEBUG LOGS
# Uncomment to print every final task assignment.
# -----------------------------------------------------

# for assignment in assignments:
#
#     print(
#         f"{assignment['employee_name']} "
#         f"-> {assignment['task_name']} "
#         f"(Final Score: {assignment['final_score']})"
#     )

print()
print("=" * 70)
print("TASK ASSIGNMENT COMPLETED")
print("=" * 70)