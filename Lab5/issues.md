# Lab 5: Issues Found and Fixed

File: `gym_membership_system.py` (original line numbers; severities as reported by each tool)

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| `eval()` on caller-supplied string (Bandit B307, Pylint W0123) | Security (Medium) | 42 | `calculateRenewalRate` runs `eval(discount_expr)`, so any string passed in executes as arbitrary Python (code injection). | Replaced with `ast.parse` plus a small whitelist evaluator that allows only numbers, `base_fee` and `+ - * /`. Anything else raises `ValueError`. |
| `os.system` with string concatenation (Bandit B605/B607) | Security (High) | 58 | `os.system("echo ... " + filename)` builds a shell command from a variable, so a filename like `x; rm -rf ~` would run extra commands. | Removed the shell call; the message is now printed with `print()`. |
| Weak hash MD5 (Bandit B324) | Security (High) | 47 | `hashlib.md5` is broken and must not be used for identifiers or security. | Switched to `hashlib.sha256`. |
| Hard-coded secret (Bandit B105) and secret printed to console | Security (Low) / Bug | 70, 79 | `gym_api_secret` is committed in source and then printed to stdout, leaking it into logs and the repo. | Read it from the `GYM_API_SECRET` environment variable and print only whether it is configured. |
| Insecure randomness (Bandit B311) | Security (Low) | 51 | `random.randint` is predictable, not suitable for a locker PIN. | Replaced with `secrets.randbelow(9000) + 1000`. |
| Mutable default argument (Pylint W0102) | Bug | 14 | `member_log=[]` is created once and shared across all calls, and the log was never read. | Default is now `None`; falls back to a module-level `MEMBER_LOG`. |
| Bare `except:` that swallows everything (Pylint W0702, Flake8 E722) | Bug / Style | 24-26 | `try: del ... except: pass` hides every error, including unrelated ones. | Replaced with `MEMBERS.pop(m_id, None)`. |
| Comparison to None with `==` (Pylint C0121, Flake8 E711) | Style | 32 | `members.get(m_id) == None` should use `is None`. | Rewritten as `member is not None and member["months_left"] > 0`, which also removes the redundant `if/else` returning True/False (R1705, line 34-37). |
| Unused variable `locker_deposit` (Pylint W0612, Flake8 F841) | Code smell | 30 | Assigned but never used. | Removed. |
| Unused import `math` (Pylint W0611, Flake8 F401) | Code smell | 5 | Imported but never used. | Removed (and unused `random` replaced by `secrets`). |
| File opened without context manager / encoding (Pylint R1732, W1514) | Bug (resource leak) | 55-57 | `open()` plus manual `close()` leaks the file handle if `write` raises; encoding not specified. | `with open(..., encoding="utf-8")`. |
| Parameter shadows global `members` (Pylint W0621) | Code smell | 61 | `get_active_summary(members)` hides the module-level dict. | Renamed the parameter to `roster` and used a generator expression with `sum`. |
| Naming convention violations (Pylint C0103) | Style | 7, 14, 22, 29, 40 | camelCase functions (`registerMember`, ...) and lowercase module-level dict `members`. | `snake_case` functions and `MEMBERS` constant. |
| Missing docstrings (Pylint C0116) | Style | all functions | No function had a docstring. | Added concise docstrings. |
| `%` string formatting (Pylint C0209) | Style | 18 | Old-style formatting. | Converted to an f-string. |
| Module runs on import (no `__main__` guard) | Design | 82 | `main()` is called at import time, so importing the module triggers the demo and file writes. | Added `if __name__ == "__main__":`. |
| Lines longer than 79 characters (Flake8 E501) | Style | 9, 10, 17 | Three lines exceed PEP 8's limit. | Wrapped the dict literals across lines. |
| Fee ignores the plan (not tool-detected) | Logic | 17 | New members pay `50.0 * months` regardless of tier, so Diana (Gold, 3 months) pays 150 while Alex (Gold, 6 months) pays 600. | Not changed because it needs a business rule from the spec; the rate is now a named constant `MONTHLY_FEE` so it is easy to make plan-based. |
