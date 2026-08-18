from ollama import chat

MODEL = "llama3.2"

SYSTEM_PROMPT = """
You are Atlas, an enterprise AI assistant.

Rules:
1. Be concise.
2. Never invent facts, definitions, acronyms, or numbers.
3. You may remember information the user explicitly tells you during this conversation.
4. If the user asks a factual question and you are uncertain, say:
   "I don't have enough reliable information to answer that."
"""

CONTEXT = """
RAG stands for Retrieval-Augmented Generation.

RAG is an AI architecture where a system retrieves relevant
information from an external knowledge source and supplies that
information to a language model before the model generates its answer.

This helps ground responses in external information instead of relying
only on the model's internal knowledge.
"""

# Conversation memory
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def ask_agent(question: str) -> str:

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = chat(
        model=MODEL,
        messages=messages
    )

    answer = response.message.content

    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return answer


print("Atlas AI Agent")
print("Type /help for commands.")

while True:
    question = input("\nYou: ").strip()

    if question == "/exit":
        print("\nGoodbye.")
        break

    if question == "/model":
        print(f"\nCurrent model: {MODEL}")
        continue

    if question == "/help":
        print("""
Commands:
/model   - show current model
/history - show number of messages in memory
/clear   - clear conversation memory
/help    - show commands
/exit    - exit Atlas
""")
        continue

    if question == "/history":
        print(f"\nMessages in memory: {len(messages)}")
        continue

    if question == "/clear":
        messages.clear()

        messages.append(
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        )

        print("\nConversation cleared.")
        continue

    if not question:
        continue

    answer = ask_agent(question)

    print(f"\nAtlas: {answer}")