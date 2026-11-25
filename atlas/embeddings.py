
import ollama

EMBEDDING_MODEL = "nomic-embed-text"


def generate_embedding(text, task="search_document"):

    # Validate that text is not empty
    if not text.strip():
        raise ValueError("Text cannot be empty.")

    # Validate that task is either search_query or search_document
    if task not in ["search_query", "search_document"]:
        raise ValueError("Task must be either 'search_query' or 'search_document'.")

    # Combine task and text using an f-string
    combined_text = f"{task}: {text}"

    # Call ollama.embed()
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input =combined_text
    )

    # Return the first embedding
    return response["embeddings"][0]
