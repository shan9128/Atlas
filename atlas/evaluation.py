
def check_answer(policy, answer):
    """Check whether the answer appears exactly in the policy."""
    if answer in policy:
        return "SUPPORTED"
    else:
        return "UNSUPPORTED"

