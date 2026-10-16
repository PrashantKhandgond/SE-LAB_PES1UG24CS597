# Lab 5 – Static Code Analysis: Gym Membership System

**Name:** PRASHANT  
**SRN:** PES1UG24CS597  
**Section:** J

## Repository
https://github.com/PrashantKhandgond/SE-LAB_PES1UG24CS597

## Tools
- Bandit – security analysis
- Pylint – code quality
- Flake8 – style/lint checks

## Files
- `gym_membership_system.py` – final corrected program (copy the verified final local version here)
- `reports/` – six actual before/after tool reports
- `Lab5_Report_PRASHANT.docx` – report with issue summary and student details

## Reproduce reports
Run in the activated virtual environment from this folder:

```powershell
python -m bandit -r gym_membership_system.py -f txt -o reports/bandit_report_after.txt
python -m pylint gym_membership_system.py > reports/pylint_report_after.txt
python -m flake8 gym_membership_system.py > reports/flake8_report_after.txt
```

For the before reports, run the same commands against the saved original file and name the outputs `*_before.txt`. Keep the real tool output; do not invent report contents.

## Commit guidance
Use separate commits for Bandit, Pylint, and Flake8 fixes as required by the lab. Push this Lab5 folder to the student's own repository, not the template repository.
