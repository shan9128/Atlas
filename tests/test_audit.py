
import logging
from atlas.audit import log_agent_event
from unittest.mock import Mock, patch
from atlas.agent import run_agent

def test_claims_audit_logging(caplog):
    with caplog.at_level(
        logging.INFO,
        logger="atlas.audit"
    ):
        log_agent_event(
            tool_name="claims_lookup",
            outcome="success"
        )

    assert "request_id=no-request" in caplog.text
    assert "Agent tool=claims_lookup outcome=success" in caplog.text
def test_claims_workflow_audit():
    mock_decision = Mock()
    mock_decision.tool = "claims_tool"
    mock_decision.model_dump.return_value = {
        "tool": "claims_tool"
    }

    with patch(
        "atlas.agent.classify_question",
        return_value=mock_decision
    ), patch(
        "atlas.agent.log_agent_event"
    ) as mock_audit:

        result = run_agent(
            "Why was claim 123 denied?"
        )

    assert result["found"] is True
    assert result["claim_id"] == "123"

    mock_audit.assert_called_once_with(
        tool_name="claims_lookup",
        outcome="found"
    )

def test_member_workflow_audit():
    mock_decision = Mock()
    mock_decision.tool = "member_tool"
    mock_decision.model_dump.return_value = {
        "tool": "member_tool"
    }

    with patch(
        "atlas.agent.classify_question",
        return_value=mock_decision
    ), patch(
        "atlas.agent.log_agent_event"
    ) as mock_audit:

        result = run_agent(
            "Is member M1001 active?"
        )

    assert result["found"] is True
    assert result["member_id"] == "M1001"

    mock_audit.assert_called_once_with(
        tool_name="member_lookup",
        outcome="found"
    )

def test_missing_claim_workflow_audit():
    mock_decision = Mock()
    mock_decision.tool = "claims_tool"
    mock_decision.model_dump.return_value = {
        "tool": "claims_tool"
    }

    with patch(
        "atlas.agent.classify_question",
        return_value=mock_decision
    ), patch(
        "atlas.agent.log_agent_event"
    ) as mock_audit:

        result = run_agent(
            "Why was claim 999 denied?"
        )

    assert result["found"] is False
    assert result["claim_id"] == "999"

    mock_audit.assert_called_once_with(
        tool_name="claims_lookup",
        outcome="not_found"
    )


def test_missing_member_workflow_audit():
    mock_decision = Mock()
    mock_decision.tool = "member_tool"
    mock_decision.model_dump.return_value = {
        "tool": "member_tool"
    }

    with patch(
        "atlas.agent.classify_question",
        return_value=mock_decision
    ), patch(
        "atlas.agent.log_agent_event"
    ) as mock_audit:

        result = run_agent(
            "Is member M9999 active?"
        )

    assert result["found"] is False
    assert result["member_id"] == "M9999"

    mock_audit.assert_called_once_with(
        tool_name="member_lookup",
        outcome="not_found"
    )

import pytest


def test_claims_lookup_error_audit():
    mock_decision = Mock()
    mock_decision.tool = "claims_tool"
    mock_decision.model_dump.return_value = {
        "tool": "claims_tool"
    }

    with patch(
        "atlas.agent.classify_question",
        return_value=mock_decision
    ), patch(
        "atlas.agent.lookup_claim",
        side_effect=ConnectionError("Database unavailable")
    ), patch(
        "atlas.agent.log_agent_event"
    ) as mock_audit:

        with pytest.raises(ConnectionError):
            run_agent("Why was claim 123 denied?")

    mock_audit.assert_called_once_with(
        tool_name="claims_lookup",
        outcome="error"
    )

def test_member_lookup_error_audit():
    mock_decision = Mock()
    mock_decision.tool = "member_tool"
    mock_decision.model_dump.return_value = {
        "tool": "member_tool"
    }

    with patch(
        "atlas.agent.classify_question",
        return_value=mock_decision
    ), patch(
        "atlas.agent.lookup_member",
        side_effect=ConnectionError("Database unavailable")
    ), patch(
        "atlas.agent.log_agent_event"
    ) as mock_audit:

        with pytest.raises(ConnectionError):
            run_agent("Is member M1001 active?")

    mock_audit.assert_called_once_with(
        tool_name="member_lookup",
        outcome="error"
    )
