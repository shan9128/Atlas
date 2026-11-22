
from pathlib import Path

POLICY_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "healthcare_policies.txt"
)


def search_policy(keyword):
    content = POLICY_FILE.read_text(encoding="utf-8")
    policies = content.strip().split("\n\n")

    for policy in policies:
        if keyword.lower() in policy.lower():
            return policy

    return "No matching policy found"


def extract_keywords(question):
    keywords = ["mri", "eligibility", "claims", "authorization"]

    words = question.lower().replace("?", "").split()
    detected_keywords = []

    for word in words:
        if word in keywords:
            detected_keywords.append(word)

    return detected_keywords


def search_multiple_policies(question):
    detected = extract_keywords(question)
    results = []

    for keyword in detected:
        policy = search_policy(keyword)

        if policy != "No matching policy found":
            if policy not in results:
                results.append(policy)

    return results

