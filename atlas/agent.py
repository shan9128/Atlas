
import re
from unittest import result

from atlas.classifier import classify_question
from atlas.tools.day3_claims_tool import lookup_claim
from atlas.tools.day4_member_tool import lookup_member
from atlas.responses.day4_response import format_member_response
from atlas.audit import log_agent_event
from atlas.tools.sqlite_claims_tool import lookup_claim_sqlite
from atlas.rag import ask_policy

def run_agent(question):

    # Explicit Kaggle claims lookup
    match = re.search(
        r"\bkaggle\s+claim\s+([A-Za-z0-9]+)\b",
        question,
        re.IGNORECASE
    )

    if match:
        claim_id = match.group(1)

        try:
            result = lookup_claim_sqlite(claim_id)
        except Exception:
            log_agent_event(
                tool_name="sqlite_claims_lookup",
                outcome="error"
            )
            raise

        log_agent_event(
            tool_name="sqlite_claims_lookup",
            outcome="found" if result["found"] else "not_found"
        )

        return result

    # Explicit healthcare policy lookup
    if "MRI" in question.upper() and "POLICY" in question.upper():
        answer = ask_policy(question, "MRI")

        log_agent_event(
            tool_name="policy_rag",
            outcome="answered"
        )

        return {
            "source": "healthcare_policies.txt",
            "answer": answer
        }

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


        try:
            result = lookup_claim(claim_id)

        except Exception:
            log_agent_event(
                tool_name="claims_lookup",
                outcome="error"
            )
            raise

        log_agent_event(
            tool_name="claims_lookup",
            outcome="found" if result.get("found") else "not_found"
        )

        return result


    elif decision.tool == "member_tool":

        match = re.search(
            r"\bmember\s+([A-Za-z0-9]+)\b",
            question,
            re.IGNORECASE
        )

        if not match:
            return {"error": "Member ID not found in question"}

        member_id = match.group(1)
    
        try:
            result = lookup_member(member_id)

        except Exception:
            log_agent_event(
                tool_name="member_lookup",
                outcome="error"
            )
            raise

        log_agent_event(
            tool_name="member_lookup",
            outcome="found" if result.get("found") else "not_found"
        )

        return result

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

