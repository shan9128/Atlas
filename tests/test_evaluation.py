
from atlas.evaluation import check_answer


def test_supported_answer():
    policy = "Outpatient MRI requires prior authorization."
    answer = "Outpatient MRI requires prior authorization."

    result = check_answer(policy, answer)

    assert result == "SUPPORTED"


def test_unsupported_answer():
    policy = "Outpatient MRI requires prior authorization."
    answer = "Outpatient MRI never requires prior authorization."

    result = check_answer(policy, answer)

    assert result == "UNSUPPORTED"

