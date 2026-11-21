
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
