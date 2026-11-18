
import re

from atlas.classifier import classify_question
from atlas.tools.day3_claims_tool import lookup_claim
from atlas.tools.day4_member_tool import lookup_member
from atlas.responses.day4_response import format_member_response

def run_agent(question):

    decision = classify_question(question)

    print("Decision:", decision.model_dump())

    if decision.tool == "claims_tool":

        match = re.search(
            r"\bclaim\s+([A-Za-z0-9]+)\b",
            question,
            re.IGNORECASE
        )

        if not match:
            return {"error": "Claim ID not found in question"}

        claim_id = match.group(1)

        return lookup_claim(claim_id)

    elif decision.tool == "member_tool":

        match = re.search(
            r"\bmember\s+([A-Za-z0-9]+)\b",
            question,
            re.IGNORECASE
        )

        if not match:
            return {"error": "Member ID not found in question"}

        member_id = match.group(1)

        return lookup_member(member_id)

    return {
        "message": "No supported tool executed",
        "decision": decision.model_dump()
    }



if __name__ == "__main__":

    question = "Is member M1001 active?"

    result = run_agent(question)

    print("Tool Result:", result)

    if "found" in result:
        answer = format_member_response(result)
        print("Atlas Answer:", answer)

