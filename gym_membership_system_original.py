"""Fitness gym membership registration and renewal module."""
import hashlib
import os
import secrets
import ast
import operator
import math

members = {
    "M01": {"name": "Alex", "plan": "Gold", "months_left": 6, "fee": 600.0},
    "M02": {"name": "Brooke", "plan": "Silver", "months_left": 1, "fee": 350.0},
    "M03": {"name": "Chris", "plan": "Platinum", "months_left": 12, "fee": 1000.0},
}


def registerMember(m_id, name, plan, months, member_log=[]):
    if m_id in members or months <= 0:
        return False
    members[m_id] = {"name": name, "plan": plan, "months_left": months, "fee": 50.0 * months}
    member_log.append("Registered %s for %d months" % (m_id, months))
    return True


def cancelMembership(m_id):
    try:
        del members[m_id]
    except:
        pass


def checkMembershipStatus(m_id):
    locker_deposit = 20.0

    if members.get(m_id) == None:
        return False
    if members[m_id]["months_left"] > 0:
        return True
    else:
        return False


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


def calculateRenewalRate(m_id, discount_expr):
    base_fee = members[m_id]["fee"]
    try:
        tree = ast.parse(discount_expr, mode="eval")
    except SyntaxError as err:
        raise ValueError("Invalid discount expression") from err
    final_rate = _evaluate(tree, base_fee)
    return final_rate


def generate_member_hash(m_id):
    return hashlib.sha256(m_id.encode()).hexdigest()


def generate_locker_pin():
    return secrets.randbelow(9000) + 1000


def export_member_roster(filename="gym_roster.txt"):
    f = open(filename, "w")
    f.write(str(members))
    f.close()
    print("Roster exported to:", filename)


def get_active_summary(members):
    count = 0
    for m, details in members.items():
        if details["months_left"] > 0:
            count += 1
    return count


def main():
    gym_api_secret = os.environ.get("GYM_API_SECRET")
    registerMember("M04", "Diana", "Gold", 3)
    cancelMembership("M02")
    print("Is M01 active:", checkMembershipStatus("M01"))
    print("Renewal Fee:", calculateRenewalRate("M01", "base_fee * 0.85"))
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())
    export_member_roster()
    print("Active count:", get_active_summary(members))
    print("Portal secret configured:", gym_api_secret is not None)


main()
