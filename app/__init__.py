from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

    app = Flask(__name__, template_folder=template_path, static_folder=static_path)
    app.secret_key = os.getenv("SECRET_KEY", "campus-connect-secret-key-change-in-production")
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = False  # Set True in production with HTTPS
    app.config["PERMANENT_SESSION_LIFETIME"] = 86400  # 24 hours

    CORS(app)

    # Register blueprints
    from app.auth import auth_bp
    from app.parents import parents_bp
    from app.student import students_bp
    from app.teacher import teachers_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(parents_bp, url_prefix="/parents")
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(teachers_bp, url_prefix="/teachers")

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import render_template
        return render_template("500.html"), 500

    return app
