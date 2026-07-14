from backend.ai_engine.services.similarity_service import calculate_similarity


def generate_recommendations(employee_vectors, task_vectors):

    recommendations = []

    # ------------------------------------------------
    # Compare every employee with every task
    # ------------------------------------------------

    for employee in employee_vectors:

        best_task = None
        best_score = -1

        for task in task_vectors:

            score = calculate_similarity(
                employee["embedding"],
                task["embedding"]
            )

            if score > best_score:
                best_score = score
                best_task = task

        # ----------------------------------------
        # Match Status
        # ----------------------------------------

        percentage = round(best_score * 100, 2)

        if percentage >= 90:
            status = "Excellent Match"

        elif percentage >= 75:
            status = "Good Match"

        elif percentage >= 60:
            status = "Average Match"

        else:
            status = "Poor Match"

        # ----------------------------------------
        # Store Recommendation
        # ----------------------------------------

        recommendations.append({

            "emp_id": employee["emp_id"],

            "task_id": best_task["task_id"],

            "task_name": best_task["task_title"],

            "similarity_score": percentage,

            "status": status

        })

    return recommendations