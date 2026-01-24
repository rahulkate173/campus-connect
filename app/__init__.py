from flask import Flask

def create_app():
    app = Flask(__name__)

    from .parents import parents_bp
    from .student import students_bp
    from .teacher import teachers_bp

    app.register_blueprint(parents_bp, url_prefix="/parents")
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(teachers_bp, url_prefix="/teachers")
    return app
