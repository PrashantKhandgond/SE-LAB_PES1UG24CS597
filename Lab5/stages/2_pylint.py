"""Gym membership system after Pylint-focused code-quality fixes."""
import ast
import hashlib
import operator
import os
import secrets

MEMBERS = {
    "M01": {"name": "Alex", "plan": "Gold", "months_left": 6, "fee": 600.0},
    "M02": {
        "name": "Brooke", "plan": "Silver", "months_left": 1, "fee": 350.0
    },
    "M03": {
        "name": "Chris", "plan": "Platinum", "months_left": 12,
        "fee": 1000.0
    },
}
MEMBER_LOG = []
MONTHLY_FEE = 50.0

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate(node, base_fee):
    """Evaluate only arithmetic operations permitted for a discount formula."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body, base_fee)
    if (isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)):
        return node.value
    if isinstance(node, ast.Name) and node.id == "base_fee":
        return base_fee
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](
            _evaluate(node.left, base_fee), _evaluate(node.right, base_fee)
        )
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.operand, base_fee))
    raise ValueError("Unsupported discount expression")


def register_member(m_id, name, plan, months, member_log=None):
    """Register a member and record the registration; reject invalid entries."""
    if member_log is None:
        member_log = MEMBER_LOG
    if m_id in MEMBERS or months <= 0:
        return False
    MEMBERS[m_id] = {
        "name": name,
        "plan": plan,
        "months_left": months,
        "fee": MONTHLY_FEE * months,
    }
    member_log.append(f"Registered {m_id} for {months} months")
    return True


def cancel_membership(m_id):
    """Remove a member if present."""
    MEMBERS.pop(m_id, None)


def check_membership_status(m_id):
    """Return whether the member exists and has months remaining."""
    member = MEMBERS.get(m_id)
    return member is not None and member["months_left"] > 0


def calculate_renewal_rate(m_id, discount_expr):
    """Calculate a renewal fee using a restricted arithmetic expression."""
    base_fee = MEMBERS[m_id]["fee"]
    try:
        tree = ast.parse(discount_expr, mode="eval")
    except SyntaxError as err:
        raise ValueError("Invalid discount expression") from err
    return _evaluate(tree, base_fee)


def generate_member_hash(m_id):
    """Return a SHA-256 digest for the member ID."""
    return hashlib.sha256(m_id.encode()).hexdigest()


def generate_locker_pin():
    """Generate a cryptographically secure four-digit locker PIN."""
    return secrets.randbelow(9000) + 1000


def export_member_roster(filename="gym_roster.txt"):
    """Write the current roster to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(MEMBERS))
    print("Roster exported to:", filename)


def get_active_summary(roster):
    """Count members who still have months remaining."""
    return sum(1 for details in roster.values() if details["months_left"] > 0)


def main():
    """Run the membership-system demonstration."""
    api_secret = os.environ.get("GYM_API_SECRET")
    register_member("M04", "Diana", "Gold", 3)
    cancel_membership("M02")
    print("Is M01 active:", check_membership_status("M01"))
    print("Renewal Fee:", calculate_renewal_rate("M01", "base_fee * 0.85"))
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())
    export_member_roster()
    print("Active count:", get_active_summary(MEMBERS))
    print("Portal secret configured:", api_secret is not None)


if __name__ == "__main__":
    main()
