
from fastapi.testclient import TestClient
from atlas.api import app

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
