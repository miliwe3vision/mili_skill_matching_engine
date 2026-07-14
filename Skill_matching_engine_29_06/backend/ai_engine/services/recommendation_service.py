from ai_engine.services.similarity_service import calculate_similarity

from ai_engine.services.matching_service import (
    language_match,
    framework_match,
    tool_match
)


# -------------------------------------------------------
# Match Status
# -------------------------------------------------------

def get_match_status(score):

    percentage = score * 100

    if percentage >= 90:
        return "Excellent Match"

    elif percentage >= 80:
        return "Strong Match"

    elif percentage >= 70:
        return "Good Match"

    elif percentage >= 60:
        return "Fair Match"

    else:
        return "Weak Match"


# -------------------------------------------------------
# Recommend Best Task
# -------------------------------------------------------

def recommend_best_task(employee, task_vectors):

    best_task = None
    highest_score = -1

    for task in task_vectors.values():

        # ---------------------------------------
        # 1. Embedding Similarity
        # ---------------------------------------

        embedding_score = calculate_similarity(
            employee["embedding"],
            task["embedding"]
        )

        # ---------------------------------------
        # 2. Programming Language Match
        # ---------------------------------------

        language_score = language_match(
            employee["programming_languages"],
            task["technologies"]
        )

        # ---------------------------------------
        # 3. Framework Match
        # ---------------------------------------

        framework_score = framework_match(
            employee["frameworks"],
            task["technologies"]
        )

        # ---------------------------------------
        # 4. Tool Match
        # ---------------------------------------

        tool_score = tool_match(
            employee["tools"],
            task["tools"]
        )

        # ---------------------------------------
        # 5. Final Weighted Score
        # ---------------------------------------

        final_score = (

            embedding_score * 0.40 +

            language_score * 0.25 +

            framework_score * 0.25 +

            tool_score * 0.10

        )

        if final_score > highest_score:

            highest_score = final_score

            best_task = {

                "task_id": task["task_id"],

                "title": task["title"],

                "embedding_score": embedding_score,

                "language_score": language_score,

                "framework_score": framework_score,

                "tool_score": tool_score,

                "score": final_score,

                "status": get_match_status(final_score)

            }

    return best_task