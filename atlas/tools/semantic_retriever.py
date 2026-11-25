from pathlib import Path
from atlas.embeddings import generate_embedding
from atlas.vector_utils import cosine_similarity

POLICY_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "healthcare_policies.txt"
)


def load_policies():

    # Read the contents of POLICY_FILE
    content = POLICY_FILE.read_text(encoding="utf-8")
    # Remove leading and trailing whitespace
    content = content.strip()
    # Split the content into individual policies
    policies = content.split("\n\n")
    # Return the list of policies
    return policies

def build_vector_index():

    # Load all policies
    policies = load_policies()
    # Create an empty list called index
    index = []
    # Loop through each policy
    for policy in policies:
        # Generate the policy embedding
        embedding = generate_embedding(policy, task="search_document")
        # Create a dictionary containing"policy" and "embedding"
        policy_dict = {"policy": policy, "embedding": embedding}
        # Append the dictionary to index    
        index.append(policy_dict)

    # Return index
    return index


def score_policies(question, index):

    # Generate the question embedding
    # Use task="search_query"
    question_embedding = generate_embedding(question, task="search_query")
    # Create an empty list called results
    results = []
    # Loop through each item in index
    for item in index:
        # Extract the policy embedding
        policy_embedding = item["embedding"]

        # Calculate cosine similarity between
        # the question and policy embeddings
        score = cosine_similarity(question_embedding, policy_embedding)

        # Create a dictionary containing
        # "policy" and "score"
        result_dict = {"policy": item["policy"], "score": score}

        # Append the dictionary to results
        results.append(result_dict)
    # Return results
    return results


def semantic_search(question, index, top_k=2):

    # Validate that top_k is greater than zero
    if top_k <= 0:
        raise ValueError("top_k must be a positive integer")

    # Call score_policies()
    results = score_policies(question, index)

    # Sort results by score in descending order
    results.sort(key=lambda x: x["score"], reverse=True)
    # Return only the top_k results
    return results[:top_k]