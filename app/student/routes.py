# app/students/routes.py
from flask import Blueprint, render_template,session,request,redirect,url_for
import os
template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
students_bp = Blueprint("students", __name__)

@students_bp.route("/")
def dashboard():
    student = {
        "name": "John Student",
        "id": "2024-UI-101",
        "initials": "JS"
    }
    return render_template("studentdashboard.html", student=student)

@students_bp.route("/status")
def status():
    return {
        "response":"student working"
    }

@students_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # TEMP authentication logic (replace with DB later)
        if email.endswith('@university.edu') and password == 'student123':
            session['user_role'] = 'student'
            session['user_email'] = email

            return redirect(url_for('students.attendance'))

        return render_template(
            'studentlogin.html',
            error="Invalid email or password"
        )

    return render_template('studentlogin.html')