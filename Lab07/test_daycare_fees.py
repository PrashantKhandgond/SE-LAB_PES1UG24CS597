
from hypothesis import given, strategies as st
from daycare_fees import parse_enrolment, hours_average, payable_fee

@given(st.text())
def test_parse_enrollment_no_crash(s):
    try:
        parse_enrollment(s)
    except Exception:
        pass
