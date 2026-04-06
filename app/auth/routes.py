from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.services.auth_service import signup_user, login_user, logout_user, get_current_user
import os

auth_bp = Blueprint("auth", __name__)

COLLEGE_DOMAIN = os.getenv("COLLEGE_DOMAIN", "pvgcoet.ac.in")


@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    """Unified login page — detects role from profile after auth."""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "student")

        if not email or not password:
            return render_template("login.html", error="Please fill in all fields", role=role)

        result = login_user(email, password)

        if result["success"]:
            user = result["user"]
            session["user"] = user
            session["access_token"] = result["access_token"]
            session.permanent = True

            # Redirect based on role
            if user["role"] == "teacher":
                return redirect(url_for("teachers.dashboard"))
            elif user["role"] == "parent":
                return redirect(url_for("parents.dashboard"))
            else:
                return redirect(url_for("students.dashboard"))
        else:
            return render_template("login.html", error=result.get("error", "Invalid credentials"), role=role)

    role = request.args.get("role", "student")
    return render_template("login.html", role=role)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup_page():
    """Student signup page."""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        full_name = request.form.get("full_name", "").strip()
        department = request.form.get("department", "").strip()
        year = request.form.get("year", "").strip()
        division = request.form.get("division", "").strip()
        roll_number = request.form.get("roll_number", "").strip()
        parent_email = request.form.get("parent_email", "").strip()
        phone = request.form.get("phone", "").strip()

        # Validation
        if not all([email, password, full_name]):
            return render_template("signup.html", error="Please fill in all required fields")

        if not email.endswith(f"@{COLLEGE_DOMAIN}"):
            return render_template("signup.html", error=f"Use your college email (@{COLLEGE_DOMAIN})")

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match")

        if len(password) < 6:
            return render_template("signup.html", error="Password must be at least 6 characters")

        result = signup_user(email, password, "student", {
            "full_name": full_name,
            "department": department,
            "year": year,
            "division": division,
            "roll_number": roll_number,
            "parent_email": parent_email,
            "phone": phone,
        })

        if result["success"]:
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("auth.login_page", role="student"))
        else:
            return render_template("signup.html", error=result.get("error", "Signup failed"))

    return render_template("signup.html")


@auth_bp.route("/logout")
def logout():
    """Log out and redirect to landing page."""
    logout_user()
    return redirect(url_for("index"))
