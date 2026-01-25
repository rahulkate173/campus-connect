from flask import Blueprint, render_template, session, request, redirect, url_for
import os
from server import view_data, create_data

students_bp = Blueprint("students", __name__, url_prefix="/students")


@students_bp.route("/")
def dashboard():
    student = {
        "name": session.get("student_name", "Student"),
        "email": session.get("student_email"),
        "initials": "ST"
    }
    return render_template("student-dashboard.html", student=student)


@students_bp.route("/status")
def status():
    return {"response": "student working"}


@students_bp.route("/login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if view_data(username=email, password=password):
            return redirect(url_for("students.dashboard"))

        return render_template(
            "studentLogin.html",
            error="Invalid email or password"
        )

    return render_template("studentLogin.html")


@students_bp.route("/signup", methods=["GET", "POST"])
def student_signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and email.endswith("@pvgcoet"):
            if create_data(username=email, password=password):
                return redirect(url_for("students.student_login"))

            return render_template(
                "studentSignup.html",
                error="User already exists"
            )

        return render_template(
            "studentSignup.html",
            error="Invalid university email"
        )

    return render_template("studentSignup.html")
