from ollama import chat


MODEL = "llama3.2"


def claims_tool(question: str):
    return {
        "tool": "claims_tool",
        "message": "Claims tool would process this request."
    }


def member_tool(question: str):
    return {
        "tool": "member_tool",
        "message": "Member tool would process this request."
    }


def provider_tool(question: str):
    return {
        "tool": "provider_tool",
        "message": "Provider tool would process this request."
    }


def rag_search(question: str):
    return {
        "tool": "rag_search",
        "message": "Knowledge search would process this request."
    }


def general_llm(question: str):

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return {
        "tool": "general_llm",
        "message": response.message.content
    }