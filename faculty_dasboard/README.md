# Faculty Backend (Flask)

A minimal Flask backend for faculty to manage branch-specific classroom and examination tasks using CSV files as storage (no Google APIs).

Features:
- Signup / Login
- Branch selection (FE/SE/TE/BE)
- Dashboard per branch
- Classroom:
  - Timetable: view, add entries
  - Assignments: add, view
  - Online Tests: add test with optional Google Form URL + upload CSV for scores
  - Attendance: add entries (student_id,status) and view analysis
- Examination: placeholder page

How to run
1. Create a virtualenv and activate it (Windows):
   python -m venv .venv
   .\.venv\Scripts\activate
2. Install dependencies:
   pip install -r requirements.txt
3. Run:
   python app.py
4. Open http://127.0.0.1:5000

Data is stored under `data/` as CSV files; for example, `assignments_BE.csv`, `attendance_SE.csv`, etc.

Notes
- This is intentionally simple and not meant for production. Passwords are stored in plain text for brevity — replace with hashed passwords in real deployments.
- You can expand the `examination` area to add schedules and marks CSV uploads similarly to online tests.
