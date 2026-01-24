# app/teachers/routes.py
from flask import Blueprint, render_template
import os
template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
teachers_bp = Blueprint("teachers", __name__,template_folder=template_path,static_folder=static_path)

@teachers_bp.route("/login")
def login():
    return render_template("facultyLogin.html")

@teachers_bp.route("/")
def dashboard():
    return render_template("facultydashboard.html")

@teachers_bp.route("/classroom")
def classroom():
    return render_template("classroom.html")

@teachers_bp.route("/attendance")
def attendance():
    return render_template("attendance.html")

@teachers_bp.route("/assignments")
def assignments():
    return render_template("assignments.html")

@teachers_bp.route("/timetable")
def timetable():
    return render_template("timetable.html")

@teachers_bp.route("/announcements")
def announcements():
    return render_template("announcements.html")

@teachers_bp.route("/internal-marks")
def internal_marks():
    return render_template("internal-marks.html")

@teachers_bp.route("/result-uploads")
def result_uploads():
    return render_template("result.html")

@teachers_bp.route("/sppu")
def sppu_coordination():
    return render_template("sppu.html")