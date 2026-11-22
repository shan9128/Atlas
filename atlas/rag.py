
import ollama

from atlas.tools.policy_retriever import search_multiple_policies


def ask_policy(question):
    policies = search_multiple_policies(question)

    if not policies:
        return "I could not find a relevant policy."

    policy = "\n\n".join(policies)

    
    prompt = f"""
            You are a healthcare payer policy assistant.

            RULES:
            1. Answer using ONLY the policies provided below.
            2. Review EVERY retrieved policy before answering.
            3. If multiple policies are relevant, explain each one.
            4. Do not invent information.
            5. If a policy does not provide an answer, say so.
            6. Include the policy ID for each answer.

            RETRIEVED POLICIES:
            {policy}

            USER QUESTION:
            {question}

            ANSWER:
            """


    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]

def ask_policy_separately(question):
    policies = search_multiple_policies(question)

    if not policies:
        return "I could not find a relevant policy."

    answers = []

    for policy in policies:
        prompt = f"""
Answer the user's question using ONLY this policy.

State what the policy explicitly says.
Do not invent rules or relationships.
If the policy answers only part of the question,
answer only that part.

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

        
        answers.append(
            f"AI ANSWER:\n{response['message']['content']}\n\n"
            f"SOURCE POLICY:\n{policy}"
        )


    return "\n\n".join(answers)
