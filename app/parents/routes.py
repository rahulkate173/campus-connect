from flask import Blueprint, render_template

parents_bp = Blueprint("parents", __name__)

@parents_bp.route("/")
def dashboard():
    return render_template("parentdashboard.html")

@parents_bp.route("/status")
def status():
    return {"response": "Welcome to Parents folder"}, 200
