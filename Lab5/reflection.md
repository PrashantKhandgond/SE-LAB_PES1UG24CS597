# Lab 5: Reflection

**1. Which issues were the easiest and which the hardest to fix?**
The easiest were the mechanical ones: removing the unused import and variable, replacing `== None` with `is None`, and switching MD5 to SHA-256. The hardest was `eval()`. The tool only says "don't use eval", but the function genuinely needs to evaluate a discount formula, so I had to design a replacement (an `ast`-based evaluator with a whitelist) and test that it blocks things like `__import__('os').system(...)`.

**2. Did the tools report any false positives or unimportant warnings?**
Some findings were low value in this context: the `random` warning (B311) is minor for a demo locker PIN, and Bandit's hard-coded secret check is a name-based heuristic. Pylint's missing-docstring and naming messages are style opinions rather than bugs. They are still cheap to fix, so I fixed them. Importantly, the tools did not flag everything: the plan-agnostic fee calculation is a logic problem only visible by reading the output and the code.

**3. How could static analysis be integrated into a real workflow?**
Run Flake8 and Pylint as a pre-commit hook and in CI (for example a GitHub Actions job) so a pull request fails if the score drops below a threshold, and run Bandit in the same pipeline so security regressions block the merge. Developers can also run them in the editor for instant feedback.

**4. What tangible improvements did you see after the fixes?**
Bandit went from High/Medium findings (command injection, `eval`, weak hash) to a clean report; Pylint's score rose to the 9.5+ target; Flake8 reports no remaining style errors. The code is also easier to read (snake_case, docstrings, early returns), safer (no shell, no `eval`, no leaked secret), and importing the module no longer runs the demo.
