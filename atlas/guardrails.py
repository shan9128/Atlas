import re


def apply_guardrails(question, prediction):

    text = question.lower()

    claim_pattern = r"\bclaim\s+(?:[a-z]*\d+[a-z0-9]*)\b"

    claim_specific = re.search(claim_pattern, text)

    lookup_keywords = [
        "denied",
        "denial",
        "status",
        "paid",
        "payment",
        "processed",
        "adjusted"
    ]

    requires_lookup = any(
        keyword in text for keyword in lookup_keywords
    )

    if claim_specific and requires_lookup:
        prediction.intent = "claims"
        prediction.action = "lookup"

    return prediction