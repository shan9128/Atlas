
def format_claim_response(result):

    if not result["found"]:
        return f"Claim {result['claim_id']} was not found."

    claim_id = result["claim_id"]
    claim = result["data"]

    status = claim["status"]

    if status == "Denied":
        return (
            f"Claim {claim_id} was denied because "
            f"{claim['denial_reason']}."
        )

    if status == "Paid":
        return (
            f"Claim {claim_id} was paid. "
            f"Allowed amount: ${claim['allowed_amount']}. "
            f"Paid amount: ${claim['paid_amount']}."
        )

    return f"Claim {claim_id} has status: {status}."
