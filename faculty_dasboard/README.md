# Faculty Backend (Flask)

as per workflow finalised at morning


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

