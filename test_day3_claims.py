
from day3_claims_tool import lookup_claim
from day3_response import format_claim_response


def test_denied_claim():
    result = lookup_claim("123")
    answer = format_claim_response(result)

    assert result["found"] is True
    assert result["data"]["status"] == "Denied"
    assert "not eligible" in answer


def test_paid_claim():
    result = lookup_claim("CLM456")
    answer = format_claim_response(result)

    assert result["found"] is True
    assert result["data"]["status"] == "Paid"
    assert "$350" in answer
    assert "$280" in answer


def test_missing_claim():
    result = lookup_claim("999")
    answer = format_claim_response(result)

    assert result["found"] is False
    assert answer == "Claim 999 was not found."
