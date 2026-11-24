
from atlas.evaluation import (
    check_answer,
    evaluate_retrieval,
    evaluate_generation
)
from unittest.mock import patch
from atlas.evaluation_runner import run_evaluation

def test_supported_answer():
    policy = "Outpatient MRI requires prior authorization."
    answer = "Outpatient MRI requires prior authorization."

    result = check_answer(policy, answer)

    assert result == "SUPPORTED"


def test_unsupported_answer():
    policy = "Outpatient MRI requires prior authorization."
    answer = "Outpatient MRI never requires prior authorization."

    result = check_answer(policy, answer)

    assert result == "UNSUPPORTED"

def test_retrieval_matching_policy():
    policies = [
        "POLICY PA-101: Prior Authorization"
    ]

    assert evaluate_retrieval(
        "PA-101", policies
    ) is True

def test_retrieval_non_matching_policy():
    policies = [
        "POLICY PA-101: Prior Authorization"
    ]

    assert evaluate_retrieval(
        "PA-102", policies
    ) is False

def test_generation_matching_answer():
    expected = "Outpatient MRI requires prior authorization."
    generated = "Outpatient MRI requires prior authorization."

    assert evaluate_generation(expected, generated) is True

def test_generation_non_matching_answer():
    expected = "Outpatient MRI requires prior authorization."
    generated = "Outpatient MRI never requires prior authorization."

    assert evaluate_generation(expected, generated) is False

def test_retrieval_empty_results():
    assert evaluate_retrieval("PA-101", []) is False


def test_generation_empty_expected():
    assert evaluate_generation("", "Some answer") is False

def test_generation_empty_generated():
    assert evaluate_generation("Some expected answer", "") is False

def test_runner_prevents_source_leakage(capsys):
    fake_response = """
AI ANSWER:
Outpatient MRI does not require prior authorization.

SOURCE POLICY:
Outpatient MRI requires prior authorization.
"""

    with patch(
        "atlas.evaluation_runner.ask_policy_separately",
        return_value=fake_response
    ):
        run_evaluation()

    output = capsys.readouterr().out

    assert "RAG-001 Generation FAIL" in output