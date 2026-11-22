from atlas.models import AtlasDecision, AtlasPrediction
from atlas.guardrails import apply_guardrails


def test_specific_claim_denial():
    prediction = AtlasPrediction(
        intent="claims",
        action="explain"
    )

    result = apply_guardrails(
        "Why was claim 123 denied?",
        prediction
    )

    assert result.intent == "claims"
    assert result.action == "lookup"


def test_general_claim_definition():
    prediction = AtlasPrediction(
        intent="claims",
        action="explain"
    )

    result = apply_guardrails(
        "What is a denied claim?",
        prediction
    )

    assert result.action == "explain"


def test_edi_definition():
    prediction = AtlasPrediction(
        intent="claims",
        action="explain"
    )

    result = apply_guardrails(
        "What is an 835 transaction?",
        prediction
    )

    assert result.action == "explain"


def test_specific_claim_cob():
    prediction = AtlasPrediction(
        intent="claims",
        action="explain"
    )

    result = apply_guardrails(
        "Was claim 5678 denied due to COB?",
        prediction
    )

    assert result.action == "lookup"

def test_claim_payment_lookup():
    prediction = AtlasPrediction(
        intent="claims",
        action="explain"
    )

    result = apply_guardrails(
        "Was claim CLM789 paid?",
        prediction
    )

    assert result.action == "lookup"


def test_general_claim_payment_explanation():
    prediction = AtlasPrediction(
        intent="claims",
        action="explain"
    )

    result = apply_guardrails(
        "How does claim payment processing work?",
        prediction
    )

    assert result.action == "explain"