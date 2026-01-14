from flask import Blueprint

bp = Blueprint("teacher", __name__, url_prefix="/teacher")

from . import routes  # noqa: F401
