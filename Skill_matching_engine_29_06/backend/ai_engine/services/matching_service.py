from ai_engine.services.embedding_service import generate_embedding
from ai_engine.services.similarity_service import calculate_similarity


# -------------------------------------------------
# Programming Language Matching
# -------------------------------------------------

def language_match(employee_languages, task_technologies):

    if not employee_languages or not task_technologies:
        return 0

    total_score = 0

    for language, rating in employee_languages.items():

        best_similarity = 0

        language_embedding = generate_embedding(language)

        for technology in task_technologies:

            technology_embedding = generate_embedding(technology)

            similarity = calculate_similarity(
                language_embedding,
                technology_embedding
            )

            if similarity > best_similarity:
                best_similarity = similarity

        weighted_similarity = best_similarity * (rating / 5)

        total_score += weighted_similarity

    return total_score / len(employee_languages)


# -------------------------------------------------
# Framework Matching
# -------------------------------------------------

def framework_match(employee_frameworks, task_technologies):

    if not employee_frameworks or not task_technologies:
        return 0

    total_score = 0

    for framework, rating in employee_frameworks.items():

        best_similarity = 0

        framework_embedding = generate_embedding(framework)

        for technology in task_technologies:

            technology_embedding = generate_embedding(technology)

            similarity = calculate_similarity(
                framework_embedding,
                technology_embedding
            )

            if similarity > best_similarity:
                best_similarity = similarity

        weighted_similarity = best_similarity * (rating / 5)

        total_score += weighted_similarity

    return total_score / len(employee_frameworks)


# -------------------------------------------------
# Tool Matching
# -------------------------------------------------

def tool_match(employee_tools, task_tools):

    if not employee_tools or not task_tools:
        return 0

    matched = 0

    for tool in employee_tools.keys():

        if tool.lower() in [t.lower() for t in task_tools]:

            matched += 1

    return matched / len(employee_tools)