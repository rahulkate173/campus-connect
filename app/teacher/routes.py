# app/teachers/routes.py
from flask import Blueprint, render_template

teachers_bp = Blueprint("teachers", __name__)

@teachers_bp.route("/")
def dashboard():
    return render_template("teacherdashboard.html")
