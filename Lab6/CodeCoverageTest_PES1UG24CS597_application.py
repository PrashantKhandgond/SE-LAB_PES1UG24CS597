
import pytest

from daycare_fees import (
    extra_hours_fee,
    enrolment_allowed,
    pickup_status
)


# ==========================================
# 1. EXTRA HOURS FEE TEST CASES
# ==========================================

def test_unknown_age_group():
    with pytest.raises(ValueError):
        extra_hours_fee("school", 30, False)


def test_negative_hours():
    with pytest.raises(ValueError):
        extra_hours_fee("toddler", -5, False)


def test_within_included_hours():
    assert extra_hours_fee("toddler", 20, False) == 0


def test_exactly_included_hours():
    assert extra_hours_fee("infant", 20, False) == 0


def test_sibling_discount():
    assert extra_hours_fee("toddler", 35, True) == 45


def test_non_infant_extra_hours():
    assert extra_hours_fee("toddler", 56, False) == 434


def test_infant_extra_hours():
    assert extra_hours_fee("infant", 45, False) == 550


def test_preschool_extra_hours():
    assert extra_hours_fee("preschool", 35, False) == 45


def test_infant_sibling_no_extra_discount():
    assert extra_hours_fee("infant", 25, True) == 70


# ==========================================
# 2. ENROLMENT ALLOWED TEST CASES
# ==========================================

def test_immunisation_pending_age_12():
    assert enrolment_allowed(12, 0, True) is True


def test_immunisation_pending_under_12():
    assert enrolment_allowed(10, 2, True) is False


def test_age_below_six_months():
    assert enrolment_allowed(5, 2, False) is False


def test_enrolment_with_vacancy():
    assert enrolment_allowed(24, 2, False) is True


def test_enrolment_without_vacancy():
    assert enrolment_allowed(24, 0, False) is False


# ==========================================
# 3. PICKUP STATUS TEST CASES
# ==========================================

def test_pickup_on_time():
    assert pickup_status(20, False, False) == "on_time"


def test_pickup_late():
    assert pickup_status(5, False, False) == "late"


def test_pickup_overdue():
    assert pickup_status(-10, False, False) == "overdue"


def test_aftercare_cutoff():
    assert pickup_status(20, True, False) == "on_time"


def test_friday_cutoff():
    assert pickup_status(10, False, True) == "late"


def test_aftercare_friday_cutoff():
    assert pickup_status(30, True, True) == "on_time"
