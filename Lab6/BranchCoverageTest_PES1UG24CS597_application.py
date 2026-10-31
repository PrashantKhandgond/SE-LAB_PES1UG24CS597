
from daycare_fees import (
    extra_hours_fee,
    enrolment_allowed,
    pickup_status
)


# ==========================================
# 1. EXTRA HOURS FEE - BRANCH COVERAGE
# ==========================================

def test_invalid_age_group():
    try:
        extra_hours_fee("school", 30, False)
        assert False
    except ValueError:
        assert True


def test_negative_hours():
    try:
        extra_hours_fee("toddler", -5, False)
        assert False
    except ValueError:
        assert True


def test_sibling_false():
    assert extra_hours_fee("toddler", 30, False) == 45


def test_sibling_true_non_infant():
    assert extra_hours_fee("toddler", 35, True) == 45


def test_sibling_true_infant():
    assert extra_hours_fee("infant", 25, True) == 70


def test_no_extra_hours():
    assert extra_hours_fee("infant", 20, False) == 0


def test_extra_hours_not_above_20():
    assert extra_hours_fee("toddler", 45, False) == 180


def test_extra_hours_above_20_non_infant():
    assert extra_hours_fee("toddler", 56, False) == 434


def test_extra_hours_above_20_infant():
    assert extra_hours_fee("infant", 45, False) == 550


def test_preschool_fee():
    assert extra_hours_fee("preschool", 35, False) == 45


# ==========================================
# 2. ENROLMENT - BRANCH COVERAGE
# ==========================================

def test_immunisation_pending_true():
    assert enrolment_allowed(12, 0, True) is True


def test_immunisation_pending_false_age():
    assert enrolment_allowed(10, 0, True) is False


def test_immunisation_not_pending():
    assert enrolment_allowed(24, 2, False) is True


def test_age_below_six():
    assert enrolment_allowed(5, 2, False) is False


def test_age_exactly_six():
    assert enrolment_allowed(6, 1, False) is True


def test_no_vacancies():
    assert enrolment_allowed(24, 0, False) is False


# ==========================================
# 3. PICKUP STATUS - BRANCH COVERAGE
# ==========================================

def test_aftercare_true():
    assert pickup_status(20, True, False) == "on_time"


def test_aftercare_false():
    assert pickup_status(10, False, False) == "on_time"


def test_friday_true():
    assert pickup_status(15, False, True) == "late"


def test_friday_false():
    assert pickup_status(10, False, False) == "on_time"


def test_pickup_on_time_boundary():
    assert pickup_status(10, False, False) == "on_time"


def test_pickup_late_boundary():
    assert pickup_status(9, False, False) == "late"


def test_pickup_overdue():
    assert pickup_status(-6, False, False) == "overdue"


def test_aftercare_late():
    assert pickup_status(10, True, False) == "late"


def test_aftercare_overdue():
    assert pickup_status(4, True, False) == "overdue"


def test_friday_on_time():
    assert pickup_status(20, False, True) == "on_time"


def test_friday_overdue():
    assert pickup_status(4, False, True) == "overdue"


def test_aftercare_friday_on_time():
    assert pickup_status(30, True, True) == "on_time"


def test_aftercare_friday_late():
    assert pickup_status(15, True, True) == "late"


def test_aftercare_friday_overdue():
    assert pickup_status(4, True, True) == "overdue"
