from flask import render_template, request

from . import bp


@bp.route("/")
def dashboard():
    return render_template("teacher/index.html")


@bp.route("/classroom/<year>")
def classroom(year=None):
    return render_template("teacher/classroom.html", year=year)


@bp.route("/exam/<year>")
def exam(year=None):
    return render_template("teacher/exam.html", year=year)
