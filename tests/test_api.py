
from fastapi.testclient import TestClient
from atlas.api import app
from unittest.mock import Mock

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "atlas-ai-agent"
    }

from unittest.mock import patch


def test_claims_endpoint():
    mock_claim = {
        "found": True,
        "claim_id": "123",
        "data": {
            "status": "Denied",
            "billed_amount": 1000,
            "allowed_amount": 0,
            "paid_amount": 0,
            "denial_reason": "Member not eligible on date of service"
        }
    }

    with patch("atlas.api.run_agent", return_value=mock_claim) as mock_agent:
        response = client.post(
            "/agent",
            json={"question": "Why was claim 123 denied?"}
        )

    assert response.status_code == 200

    assert response.json() == {
        "question": "Why was claim 123 denied?",
        "answer": "Claim 123 was denied because Member not eligible on date of service."
    }

    mock_agent.assert_called_once_with("Why was claim 123 denied?")

def test_member_endpoint():
    mock_member = {
        "found": True,
        "member_id": "M1001",
        "data": {
            "name": "John Smith",
            "status": "Active",
            "plan": "Gold",
            "effective_date": "2026-01-01"
        }
    }

    with patch("atlas.api.run_agent", return_value=mock_member) as mock_agent:
        response = client.post(
            "/agent",
            json={"question": "Is member M1001 active?"}
        )

    assert response.status_code == 200

    assert response.json() == {
        "question": "Is member M1001 active?",
        "answer": (
            "Member M1001 (John Smith) has a recorded status "
            "of Active under the Gold plan, effective 2026-01-01."
        )
    }

    mock_agent.assert_called_once_with("Is member M1001 active?")

def test_missing_question():
    response = client.post("/agent", json={})

    assert response.status_code == 422


def test_invalid_question_type():
    response = client.post(
        "/agent",
        json={"question": 123}
    )

    assert response.status_code == 422

def test_empty_question():
    response = client.post(
        "/agent",
        json={"question": ""}
    )

    assert response.status_code == 422


def test_whitespace_question():
    response = client.post(
        "/agent",
        json={"question": "   "}
    )

    assert response.status_code == 422


from httpx import ConnectError


def test_agent_service_unavailable():
    with patch(
        "atlas.api.run_agent",
        side_effect=ConnectError("Ollama unavailable")
    ):
        response = client.post(
            "/agent",
            json={"question": "Why was claim 123 denied?"}
        )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Atlas AI service is temporarily unavailable"
    }

def test_agent_internal_error():
    with patch(
        "atlas.api.run_agent",
        side_effect=RuntimeError("Internal database details")
    ):
        response = client.post(
            "/agent",
            json={"question": "Why was claim 123 denied?"}
        )

    assert response.status_code == 500

    assert response.json() == {
        "detail": "Atlas encountered an internal processing error"
    }

    assert "Internal database details" not in response.text

def test_full_claims_api_integration():
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

        response = client.post(
            "/agent",
            json={"question": "Why was claim 123 denied?"}
        )

    assert response.status_code == 200

    assert response.json()["answer"] == (
        "Claim 123 was denied because "
        "Member not eligible on date of service."
    )

    mock_audit.assert_called_once_with(
        tool_name="claims_lookup",
        outcome="found"
    )


from uuid import UUID


def test_request_id_header():
    response = client.get("/health")

    assert response.status_code == 200

    request_id = response.headers["X-Request-ID"]

    assert UUID(request_id).version == 4


def test_request_id_matches_audit_log(caplog):
    mock_decision = Mock()
    mock_decision.tool = "claims_tool"
    mock_decision.model_dump.return_value = {
        "tool": "claims_tool"
    }

    with patch(
        "atlas.agent.classify_question",
        return_value=mock_decision
    ), caplog.at_level("INFO", logger="atlas.audit"):

        response = client.post(
            "/agent",
            json={"question": "Why was claim 123 denied?"}
        )

    assert response.status_code == 200

    request_id = response.headers["X-Request-ID"]

    assert f"request_id={request_id}" in caplog.text
    assert "Agent tool=claims_lookup outcome=found" in caplog.text
