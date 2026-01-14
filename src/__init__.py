from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template
from pathlib import Path
from .config import Config


def create_app():
    # Create Flask app with absolute template/static folders (project root)
    project_root = Path(__file__).resolve().parents[1]
    template_dir = str(project_root / "templates")
    static_dir = str(project_root / "static")
    flask_app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    flask_app.config.from_object(Config)

    # Import and register blueprints
    from .auth import bp as auth_bp

    flask_app.register_blueprint(auth_bp)

    from .student import bp as student_bp

    flask_app.register_blueprint(student_bp)

    from .parent import bp as parent_bp

    flask_app.register_blueprint(parent_bp)

    from .teacher import bp as teacher_bp

    flask_app.register_blueprint(teacher_bp)

    # add a simple root route
    @flask_app.route("/")
    def index():
        return render_template("index.html")

    # Create FastAPI app and mount API + Flask WSGI app
    api_app = FastAPI(title="Campus Connect API")

    from .api import router as api_router

    api_app.include_router(api_router, prefix="/api")

    api_app.mount("/", WSGIMiddleware(flask_app))

    return api_app
