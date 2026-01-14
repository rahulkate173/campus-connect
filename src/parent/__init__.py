from flask import Blueprint

bp = Blueprint("parent", __name__, url_prefix="/parent")

from . import routes  # noqa: F401
