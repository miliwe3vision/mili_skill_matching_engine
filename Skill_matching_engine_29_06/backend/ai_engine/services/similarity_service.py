from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(employee_embedding, task_embedding):

    similarity = cosine_similarity(

        [employee_embedding],
        [task_embedding]

    )[0][0]

    return float(similarity)