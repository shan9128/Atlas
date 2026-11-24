
import json
from pathlib import Path

from atlas.evaluation import (
    evaluate_retrieval,
    evaluate_generation
)
from atlas.tools.policy_retriever import search_multiple_policies
from atlas.rag import ask_policy_separately

BASE_DIR = Path(__file__).resolve().parents[1]
EVAL_FILE = BASE_DIR / "data" / "rag_evaluation.json"


def run_evaluation():
    with open(EVAL_FILE, "r") as file:
        evaluation_data = json.load(file)

    passed = 0
    failed = 0
    generation_passed = 0
    generation_failed = 0
    
    for case in evaluation_data:
        question = case["question"]
        expected_policy = case["expected_policy"]

        actual_policies = search_multiple_policies(question)
        result = evaluate_retrieval(
            expected_policy, actual_policies
        )

        expected_answer = case["expected_answer"]

        response = ask_policy_separately(question)
        resp = response.split("SOURCE POLICY:")

        # Split the response and extract the AI answer
        if len(resp) > 1:
            generated_answer = resp[0].replace("AI ANSWER:", "").strip()
        else:
            generated_answer = ""

        # Evaluate the generated answer
        generation_result = evaluate_generation(expected_answer, generated_answer)
        print("Expected:", expected_answer)
        print("Generated:", generated_answer)
        # Increment generation_passed or generation_failed
        if generation_result:
            generation_passed += 1
        else:
            generation_failed += 1
        # Print the generation evaluation result
        if generation_result:
            print(case["id"], "Generation PASS")
        else:
            print(case["id"], "Generation FAIL")

        if result:
            print(case["id"], "PASS")
            passed += 1
        else:
            print(case["id"], "FAIL")
            failed += 1

    total = len(evaluation_data)
    hit_rate = (passed / total) * 100 if total else 0

    print("\nTotal:", total)
    print("Passed:", passed)
    print("Failed:", failed)
    print("Retrieval Hit Rate:", hit_rate, "%")
    generation_rate = (    generation_passed / total * 100 if total else 0)
    print("\nGeneration Evaluation")
    print("Passed:", generation_passed)
    print("Failed:", generation_failed)
    print("Generation Match Rate:", generation_rate, "%")

if __name__ == "__main__":
    run_evaluation()

