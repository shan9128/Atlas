
from unittest.mock import patch
from atlas.agent import run_agent


def test_mri_policy_routing():
    with patch("atlas.agent.ask_policy") as mock_rag:
        mock_rag.return_value = "Outpatient MRI requires prior authorization."

        result = run_agent(
            "According to the policy, does outpatient MRI require authorization?"
        )

        assert result["source"] == "healthcare_policies.txt"
        assert "requires prior authorization" in result["answer"]

        mock_rag.assert_called_once()
