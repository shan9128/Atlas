
from unittest.mock import patch
from types import SimpleNamespace

from atlas.classifier import classify_question


def test_classifier_retries_invalid_prediction():

    invalid_response = SimpleNamespace(
        message=SimpleNamespace(
            content='{"intent":"general","action":"lookup"}'
        )
    )

    valid_response = SimpleNamespace(
        message=SimpleNamespace(
            content='{"intent":"claims","action":"lookup"}'
        )
    )

    with patch(
        "atlas.classifier.chat",
        side_effect=[invalid_response, valid_response]
    ) as mock_chat:

        decision = classify_question(
            "Explain the claims adjudication process."
        )

    assert decision.intent == "claims"
    assert decision.action == "lookup"
    assert decision.needs_tool is True
    assert decision.tool == "claims_tool"

    assert mock_chat.call_count == 2
