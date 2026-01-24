from flask import Flask
import os

def create_app():
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    app = Flask(__name__,template_folder=template_path,static_folder=static_path)

    from .parents import parents_bp
    from .student import students_bp
    from .teacher import teachers_bp

    app.register_blueprint(parents_bp, url_prefix="/parents")
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(teachers_bp, url_prefix="/teachers")
    return app
