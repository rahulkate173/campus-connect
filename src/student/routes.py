from flask import render_template, Blueprint

from . import bp


@bp.route("/")
def dashboard():
    return render_template("student/index.html")


@bp.route("/classroom")
def classroom():
    return render_template("student/classroom.html")


@bp.route("/exam")
def exam():
    return render_template("student/examination.html")


@bp.route("/career")
def career():
    return render_template("student/career.html")
