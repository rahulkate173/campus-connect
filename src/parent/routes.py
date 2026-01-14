from flask import render_template

from . import bp


@bp.route("/")
def dashboard():
    return render_template("parent/index.html")


@bp.route("/academics")
def academics():
    return render_template("parent/academics.html")


@bp.route("/attendance")
def attendance():
    return render_template("parent/attendance.html")
