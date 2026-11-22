from ollama import chat

MODEL = "llama3.2"


# def ask_atlas(question: str) -> str:
#     response = chat(
#         model=MODEL,
#         messages=[
#             {
#                 "role": "system",
#                 "content": (        
#         "You are Atlas, an AI engineering assistant. "
#         "In this conversation, RAG means Retrieval-Augmented Generation. "
#         "Focus on LLMs, AI agents, Python, MCP, and enterprise AI. "
#         "Give concise, technically accurate explanations. "
#         "If you are unsure, acknowledge uncertainty. "
#         "Do not invent technical definitions or code.")
#             },
#             {
#                 "role": "user",
#                 "content": question
#             }
#         ]
#     )

#     return response.message.content


# if __name__ == "__main__":
#     while True:
#         question = input("You: ").strip()

#         if question.lower() == "/exit":
#             print("Atlas: Goodbye!")
#             break

#         if not question:
#             continue
#         answer = ask_atlas(question)
#         print("Atlas:", answer)

def ask_atlas(question: str, messages: list) -> str:
    messages.append({
        "role": "user",
        "content": question
    })

    response = chat(
        model=MODEL,
        messages=messages
    )

    answer = response.message.content

    messages.extend([
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer}
    ])

    return answer

if __name__ == "__main__":

    messages = [
        {
            "role": "system",
            "content": ("You are Atlas, a helpful AI assistant."
                        "Explain technical concepts accurately and clearly.")
        }
    ]

    while True:
        question = input("You: ").strip()

        if question.lower() == "/exit":
            break

        if not question:
            continue

        try:
            answer = ask_atlas(question, messages)
            print("Atlas:", answer)

        except Exception as error:
            # Remove the latest user message if the model call failed.
            if messages and messages[-1]["role"] == "user":
                messages.pop()

            print("Atlas error:", error)