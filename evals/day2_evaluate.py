import json
from atlas.classifier import classify_question


with open("evals/day2_evals.json", "r") as file:
    test_cases = json.load(file)

intent_correct = 0
action_correct = 0
tool_correct = 0
correct = 0
total = len(test_cases)

for case in test_cases:
    question = case["question"]

    try:
        decision = classify_question(question)
        if decision.intent == case["expected_intent"]:
            intent_correct += 1

        if decision.action == case["expected_action"]:
            action_correct += 1

        if decision.tool == case["expected_tool"]:
            tool_correct += 1
        passed = (
            decision.intent == case["expected_intent"]
            and decision.action == case["expected_action"]
            and decision.tool == case["expected_tool"]
        )

        if passed:
            correct += 1

        print(f"Question: {question}")
        print(f"Expected: {case['expected_intent']}, "
              f"{case['expected_action']}, "
              f"{case['expected_tool']}")
        print(f"Actual: {decision.intent}, "
              f"{decision.action}, "
              f"{decision.tool}")
        print("PASS" if passed else "FAIL")
        print("-" * 40)

    except Exception as error:
        print(f"Question: {question}")
        print(f"ERROR: {error}")
        print("-" * 40)

accuracy = (correct / total) * 100 if total else 0

print(f"\nEvaluation Accuracy: {accuracy:.1f}%")
print(f"Correct: {correct}/{total}")
print("\n--- ATLAS EVALUATION REPORT ---")

print(f"Overall Accuracy: {correct / total * 100:.1f}%")
print(f"Intent Accuracy: {intent_correct / total * 100:.1f}%")
print(f"Action Accuracy: {action_correct / total * 100:.1f}%")
print(f"Tool Accuracy: {tool_correct / total * 100:.1f}%")