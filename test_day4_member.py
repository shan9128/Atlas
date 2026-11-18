
from day4_member_tool import lookup_member
from day4_response import format_member_response


def test_active_member():
    result = lookup_member("M1001")
    answer = format_member_response(result)

    assert result["found"] is True
    assert result["data"]["status"] == "Active"
    assert "Gold" in answer


def test_inactive_member():
    result = lookup_member("M2002")
    answer = format_member_response(result)

    assert result["found"] is True
    assert result["data"]["status"] == "Inactive"
    assert "Silver" in answer


def test_missing_member():
    result = lookup_member("M9999")
    answer = format_member_response(result)

    assert result["found"] is False
    assert answer == "Member M9999 was not found."
