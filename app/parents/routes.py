from flask import Blueprint, render_template

parents_bp = Blueprint("parents", __name__)

@parents_bp.route("/")
def dashboard():
    return render_template("parentdashboard.html")

@parents_bp.route("/attendance")
def attendance():
    return render_template("parent-attendance.html")

@parents_bp.route("/academics")
def academics():
    return render_template("parentsAcademics.html")

@parents_bp.route("/announcements")
def announcements():
    return render_template("parent-announcement.html")



