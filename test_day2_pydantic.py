import pytest
from pydantic import ValidationError
from day2_pydantic import AtlasDecision


def test_valid_claim_lookup():
    decision = AtlasDecision(
        intent="claims",
        action="lookup",
        needs_tool=True,
        tool="claims_tool"
    )

    assert decision.intent == "claims"
    assert decision.tool == "claims_tool"


def test_invalid_claims_tool():
    with pytest.raises(ValidationError):
        AtlasDecision(
            intent="claims",
            action="lookup",
            needs_tool=True,
            tool="member_tool"
        )


def test_invalid_explain_with_tool():
    with pytest.raises(ValidationError):
        AtlasDecision(
            intent="claims",
            action="explain",
            needs_tool=True,
            tool="claims_tool"
        )

def test_invalid_lookup_without_tool():
    with pytest.raises(ValidationError):
        AtlasDecision(
            intent="claims",
            action="lookup",
            needs_tool=False,
            tool="none"
        )