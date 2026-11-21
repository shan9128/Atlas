
import ollama

from atlas.tools.policy_retriever import search_policy


def ask_policy(question, keyword):
    policy = search_policy(keyword)

    if policy == "No matching policy found":
        return "I could not find a relevant policy."

    prompt = f"""
You are a healthcare payer policy assistant.

Answer the question using ONLY the policy below.
Do not invent additional policy rules.
If the policy does not answer the question, say so.

POLICY:
{policy}

QUESTION:
{question}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
