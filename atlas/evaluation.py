
def check_answer(policy, answer):
    """Check whether the answer appears exactly in the policy."""
    if answer in policy:
        return "SUPPORTED"
    else:
        return "UNSUPPORTED"


def check_answer(policy, answer):
    """Check whether the answer appears exactly in the policy."""
    if answer in policy:
        return "SUPPORTED"
    else:
        return "UNSUPPORTED"


def evaluate_retrieval(expected_policy, actual_policies):
    """Check whether the expected policy was retrieved."""
    found = False

    for policy in actual_policies:
        if expected_policy in policy:
            found = True
            break

    return found

def evaluate_generation(expected_answer, generated_answer):
    if not expected_answer.strip():
        return False

    return expected_answer.lower() in generated_answer.lower()
