from ai_engine.data.tasks import tasks
from ai_engine.utils.text_builder import build_task_text
from ai_engine.services.embedding_service import generate_embedding
from ai_engine.services.vector_storage_service import save_task_vector


def generate_task_embeddings():

    task_vectors = {}

    print("\nGenerating Task Embeddings...\n")

    for task in tasks:

        # -----------------------------------
        # Convert Task -> Text
        # -----------------------------------
        text = build_task_text(task)

        # -----------------------------------
        # Generate Embedding
        # -----------------------------------
        embedding = generate_embedding(text)

        # -----------------------------------
        # SAFE ID handling
        # -----------------------------------
        task_id = task["id"]

        # -----------------------------------
        # Save Vector to Supabase
        # -----------------------------------
        save_task_vector(
            task_id,
            task["title"],
            embedding
        )

        # -----------------------------------
        # Store Locally
        # -----------------------------------
        task_vectors[task_id] = {

            "id": task_id,
            "title": task.get("title"),
            "description": task.get("description"),

            "technologies": task.get("technologies", []),
            "tools": task.get("tools", []),
            "required_skills": task.get("required_skills", []),

            "text": text,
            "embedding": embedding
        }

        print(f"✓ {task.get('title')}")

    return task_vectors