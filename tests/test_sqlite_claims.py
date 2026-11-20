
import sqlite3
import pytest
from unittest.mock import patch
from unittest.mock import Mock
from atlas.agent import run_agent

from atlas.tools.sqlite_claims_tool import lookup_claim_sqlite


def test_sqlite_database_unavailable():
    with patch(
        "atlas.tools.sqlite_claims_tool.sqlite3.connect",
        side_effect=sqlite3.OperationalError("Database unavailable")
    ):
        with pytest.raises(
            sqlite3.OperationalError,
            match="Database unavailable"
        ):
            lookup_claim_sqlite("18874")

def test_sqlite_valid_claim():
    result = lookup_claim_sqlite("18874")

    assert result["found"] is True
    assert result["claim_id"] == "18874"
    assert result["patient_id"] == "67349080"
    assert result["claim_amount"] == 462337.48


def test_sqlite_conflicting_claim():
    result = lookup_claim_sqlite("10782")

    assert result == {
        "found": False,
        "claim_id": "10782"
    }


def test_agent_sqlite_integration():
    with patch(
        "atlas.agent.log_agent_event"
    ) as mock_audit:

        result = run_agent("Look up Kaggle claim 18874")

    assert result["found"] is True
    assert result["claim_id"] == "18874"

    mock_audit.assert_called_once_with(
        tool_name="sqlite_claims_lookup",
        outcome="found"
    )
