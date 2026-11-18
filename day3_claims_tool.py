
from day3_claims_data import CLAIMS


def lookup_claim(claim_id):
    claim = CLAIMS.get(claim_id)

    if claim is None:
        return {
            "found": False,
            "claim_id": claim_id,
            "message": "Claim not found"
        }

    return {
        "found": True,
        "claim_id": claim_id,
        "data": claim
    }


if __name__ == "__main__":
    print(lookup_claim("123"))
    print(lookup_claim("999"))
