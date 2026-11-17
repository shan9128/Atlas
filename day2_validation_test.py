from pydantic import ValidationError
from day2_pydantic import AtlasDecision


test_cases = [
    {
        "intent": "claims",
        "action": "lookup",
        "needs_tool": True,
        "tool": "member_tool"
    },
    {
        "intent": "claims",
        "action": "lookup",
        "needs_tool": True,
        "tool": "claims_tool"
    },
    {
        "intent": "claims",
        "action": "explain",
        "needs_tool": True,
        "tool": "claims_tool"
    }
]


for index, data in enumerate(test_cases, start=1):
    print(f"\nTest {index}")

    try:
        decision = AtlasDecision(**data)
        print("ACCEPTED:", decision.model_dump())
    except ValidationError as error:
        print("REJECTED:", error.errors()[0]["msg"])