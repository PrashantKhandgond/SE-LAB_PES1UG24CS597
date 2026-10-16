"""Gym membership system after Bandit-focused security fixes."""
import ast
import hashlib
import operator
import os
import secrets

MEMBERS = {
    "M01": {"name": "Alex", "plan": "Gold", "months_left": 6, "fee": 600.0},
    "M02": {"name": "Brooke", "plan": "Silver", "months_left": 1, "fee": 350.0},
    "M03": {"name": "Chris", "plan": "Platinum", "months_left": 12, "fee": 1000.0},
}

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate(node, base_fee):
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


def registerMember(m_id, name, plan, months, member_log=None):
    if member_log is None:
        member_log = []
    if m_id in MEMBERS or months <= 0:
        return False
    MEMBERS[m_id] = {
        "name": name, "plan": plan, "months_left": months, "fee": 50.0 * months
    }
    member_log.append(f"Registered {m_id} for {months} months")
    return True


def cancelMembership(m_id):
    MEMBERS.pop(m_id, None)


def checkMembershipStatus(m_id):
    member = MEMBERS.get(m_id)
    return member is not None and member["months_left"] > 0


def calculateRenewalRate(m_id, discount_expr):
    base_fee = MEMBERS[m_id]["fee"]
    try:
        tree = ast.parse(discount_expr, mode="eval")
    except SyntaxError as err:
        raise ValueError("Invalid discount expression") from err
    return _evaluate(tree, base_fee)


def generate_member_hash(m_id):
    return hashlib.sha256(m_id.encode()).hexdigest()


def generate_locker_pin():
    return secrets.randbelow(9000) + 1000


def export_member_roster(filename="gym_roster.txt"):
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(MEMBERS))
    print("Roster exported to:", filename)


def get_active_summary(roster):
    return sum(1 for details in roster.values() if details["months_left"] > 0)


def main():
    api_secret = os.environ.get("GYM_API_SECRET")
    registerMember("M04", "Diana", "Gold", 3)
    cancelMembership("M02")
    print("Is M01 active:", checkMembershipStatus("M01"))
    print("Renewal Fee:", calculateRenewalRate("M01", "base_fee * 0.85"))
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())
    export_member_roster()
    print("Active count:", get_active_summary(MEMBERS))
    print("Portal secret configured:", api_secret is not None)


if __name__ == "__main__":
    main()
