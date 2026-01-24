# app/students/routes.py
from flask import Blueprint, render_template

students_bp = Blueprint("students", __name__)

@students_bp.route("/")
def dashboard():
    student = {
        "name": "John Student",
        "id": "2024-UI-101",
        "initials": "JS"
    }
    return render_template("studentdashboard.html", student=student)
