from backend.ai_engine.services.similarity_service import calculate_similarity


def generate_recommendations(employee_vectors, task_vectors):

    recommendations = []

    # ------------------------------------------------
    # DEBUG
    # Uncomment to display similarity generation.
    # ------------------------------------------------

    # print("\nGenerating Employee-Task Similarity Matrix...\n")

    # ------------------------------------------------
    # Compare EVERY employee with EVERY task
    # ------------------------------------------------

    for employee in employee_vectors:

        for task in task_vectors:

            # ----------------------------------------
            # Calculate Cosine Similarity
            # ----------------------------------------

            score = calculate_similarity(
                employee["embedding"],
                task["embedding"]
            )

            percentage = round(score * 100, 2)

            # ----------------------------------------
            # Match Status
            # ----------------------------------------

            if percentage >= 90:
                status = "Excellent Match"

            elif percentage >= 75:
                status = "Good Match"

            elif percentage >= 60:
                status = "Average Match"

            else:
                status = "Poor Match"

            # ----------------------------------------
            # Store Every Combination
            # ----------------------------------------

            recommendations.append({

                "emp_id": employee["emp_id"],

                "task_id": task["task_id"],

                "task_name": task["task_title"],

                "similarity_score": percentage,

                "status": status

            })

            # ------------------------------------------------
            # DEBUG
            # Uncomment to see similarity score for every
            # Employee ↔ Task combination.
            # ------------------------------------------------

            # print(
            #     f"✓ Employee {employee['emp_id']} "
            #     f"↔ {task['task_title']} "
            #     f"({percentage}%)"
            # )

    # ------------------------------------------------
    # DEBUG
    # Uncomment to display total similarity records.
    # ------------------------------------------------

    # print(f"\nTotal Similarity Records : {len(recommendations)}")

    return recommendations