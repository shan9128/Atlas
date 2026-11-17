from day2_router import build_decision


tests = [
    ("claims", "lookup"),
    ("claims", "explain"),
    ("member", "lookup"),
    ("member", "explain"),
    ("general", "explain"),
    ("general", "lookup")
]


for intent, action in tests:
    print(f"\nInput: {intent}, {action}")

    try:
        decision = build_decision(intent, action)
        print(decision.model_dump_json(indent=2))

    except ValueError as error:
        print("REJECTED:", error)

print("\nTesting unsupported lookup:")

try:
    decision = build_decision("general", "lookup")
    print(decision)

except ValueError as error:
    print("Correctly rejected:", error)