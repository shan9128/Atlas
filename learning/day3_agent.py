
import re

from atlas.classifier import classify_question
from atlas.tools.day3_claims_tool import lookup_claim
from atlas.responses.day3_response import format_claim_response


def run_agent(question):

    # Step 1: Ask Atlas to classify the question
    decision = classify_question(question)

    print("Decision:", decision.model_dump())

    # Step 2: Check whether claims_tool was selected
    if decision.tool == "claims_tool":

        # Step 3: Extract claim ID from the question
        match = re.search(
            r"\bclaim\s+([A-Za-z0-9]+)\b",
            question,
            re.IGNORECASE
        )

        if not match:
            return {
                "error": "Could not identify claim ID"
            }

        claim_id = match.group(1)

        # Step 4: Execute our claims lookup tool
        return lookup_claim(claim_id)

    return {
        "message": "No supported tool executed",
        "decision": decision.model_dump()
    }


if __name__ == "__main__":

    question = "What is the status of claim 999?"

    result = run_agent(question)

    print("Tool Result:", result)

    if "found" in result:
        answer = format_claim_response(result)
        print("Atlas Answer:", answer)