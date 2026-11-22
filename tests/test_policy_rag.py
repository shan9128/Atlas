
from unittest.mock import patch
from atlas.agent import run_agent


def test_mri_policy_routing():
    with patch("atlas.agent.ask_policy_separately") as mock_rag:
        mock_rag.return_value = "Outpatient MRI requires prior authorization."

        result = run_agent(
            "According to the policy, does outpatient MRI require authorization?"
        )

        assert result["source"] == "healthcare_policies.txt"
        assert "requires prior authorization" in result["answer"]

        mock_rag.assert_called_once()


def test_member_eligibility_uses_member_tool():
    result = run_agent("Check eligibility for member M1001")

    assert result["found"] is True
    assert result["member_id"] == "M1001"
    assert result["data"]["status"] == "Active"
