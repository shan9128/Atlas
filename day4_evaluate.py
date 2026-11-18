
import json

from day2_classifier import classify_question
from day4_agent import run_agent
from day3_response import format_claim_response
from day4_response import format_member_response


with open("day4_evals.json", "r") as file:
    evaluations = json.load(file)


passed = 0

for test in evaluations:

    question = test["question"]

    print("\nQuestion:", question)

    # Check which tool Atlas selects
    decision = classify_question(question)

    # Execute the agent
    result = run_agent(question)

    # Format the response using the selected tool
    if decision.tool == "claims_tool":
        answer = format_claim_response(result)

    elif decision.tool == "member_tool":
        answer = format_member_response(result)

    else:
        answer = str(result)

    # Check the expected result
    tool_correct = decision.tool == test["expected_tool"]

    found_correct = (
        result.get("found") == test["expected_found"]
    )

    answer_correct = all(
        keyword.lower() in answer.lower()
        for keyword in test["expected_answer_contains"]
    )

    if tool_correct and found_correct and answer_correct:
        print("PASS")
        passed += 1
    else:
        print("FAIL")
        print("Tool correct:", tool_correct)
        print("Found correct:", found_correct)
        print("Answer correct:", answer_correct)

    print("Atlas Answer:", answer)
    print("-" * 40)


total = len(evaluations)

print("\n--- DAY 4 EVALUATION REPORT ---")
print(f"Passed: {passed}/{total}")
print(f"Accuracy: {passed / total * 100:.1f}%")
