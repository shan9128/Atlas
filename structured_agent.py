import json
import pydantic
from ollama import chat
from typing import Literal
from pydantic import BaseModel, Field, ValidationError

MODEL = "llama3.2"

SYSTEM_PROMPT = """
You are Atlas, an enterprise AI assistant.

Classify the user's request into exactly ONE intent.

Allowed intents:
- claims
- member
- provider
- rag
- general

Return ONLY valid JSON in exactly this structure:

{
  "intent": "claims",
  "needs_tool": true,
  "priority": "low",
  "confidence": 0.95
}

Rules:
1. intent MUST be exactly one of:
   claims, member, provider, rag, general
2. Do NOT combine intents.
   Wrong: "claims | denied"
   Wrong: "claims denied"
   Wrong: "claim"
   Correct: "claims"
3. priority MUST be exactly one of:
   low, medium, high
4. confidence MUST be between 0.0 and 1.0.
5. Return JSON only.
6. Do not include markdown.
7. Do not include explanations.
"""

class Classification(BaseModel):
    intent: Literal["claims", "member", "provider", "rag", "general"]
    needs_tool: bool
    priority: Literal["low", "medium", "high"]
    confidence: float = Field(ge=0.0, le=1.0)

def classify_with_llm(question: str) -> dict:
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    raw_output = response.message.content

    # print("\nRAW MODEL OUTPUT:")
    # print(raw_output)

    try:
        result = json.loads(raw_output)
        return result

    except json.JSONDecodeError:
        return {
            "intent": "general",
            "needs_tool": False,
            "priority": "low",
            "confidence": 0.0,
            "error": "Model returned invalid JSON"
        }

question = input("Ask Atlas: ")

result = classify_with_llm(question)

# print("\nPARSED RESULT:")
# print(result)

def route_request(classification: Classification) -> str:
    if classification.intent == "claims":
        return "Route to claims tool"
    elif classification.intent == "member":
        return "member_tool"
    elif classification.intent == "provider":
        return "provider_tool"
    elif classification.intent == "rag":
        return "Route to knowledge search"
    else:
        return "Use general response"


try:
    validated = Classification(**result)

    print("\nClassification:")
    print(f"intent='{validated.intent}'")
    print(f"needs_tool={validated.needs_tool}")
    print(f"priority='{validated.priority}'")
    print(f"confidence={validated.confidence}")

    route = route_request(validated)

    print("\nROUTING DECISION:")
    print(f"Selected route: {route}")

except ValidationError as error:
    print("\nValidation failed:")
    print(error)
