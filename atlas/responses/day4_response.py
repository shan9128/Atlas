
def format_member_response(result):

    if not result["found"]:
        return f"Member {result['member_id']} was not found."

    member_id = result["member_id"]
    member = result["data"]

    name = member["name"]
    status = member["status"]
    plan = member["plan"]
    effective_date = member["effective_date"]

    return (
        f"Member {member_id} ({name}) has a recorded "
        f"status of {status} under the {plan} plan, "
        f"effective {effective_date}."
    )
