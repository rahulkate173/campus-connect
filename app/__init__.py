"""
Flask application factory for Campus Connect
"""
from flask import Flask
from flask_cors import CORS
import os

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-this')
    app.config['DEBUG'] = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Enable CORS for cross-origin requests
    CORS(app)
    
    # Register blueprints
    from app.routes import auth, student, faculty, parent
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(student.bp, url_prefix='/student')
    app.register_blueprint(faculty.bp, url_prefix='/faculty')
    app.register_blueprint(parent.bp, url_prefix='/parent')
    
    # Home route
    from flask import render_template
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
