"""
Authentication routes for Campus Connect
"""
from flask import Blueprint, request, jsonify, render_template, session
from app.services.supabase_service import SupabaseService
import asyncio

bp = Blueprint('auth', __name__)
supabase_service = SupabaseService()

# Login page routes
@bp.route('/student-login')
def student_login():
    """Render student login page"""
    return render_template('studentLogin.html')

@bp.route('/faculty-login')
def faculty_login():
    """Render faculty login page"""
    return render_template('facultyLogin.html')

@bp.route('/parent-login')
def parent_login():
    """Render parent login page"""
    return render_template('parentLogin.html')

# API routes
@bp.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"success": False, "error": "Email and password are required"}), 400
        
        # Sign in with Supabase
        result = asyncio.run(supabase_service.sign_in(email, password))
        
        if result.get('success'):
            # Store user session
            user_data = result.get('data')
            session['user'] = {
                'id': user_data.user.id if hasattr(user_data, 'user') else None,
                'email': email
            }
            return jsonify(result), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    try:
        result = asyncio.run(supabase_service.sign_out())
        session.clear()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    """Get user profile"""
    try:
        result = asyncio.run(supabase_service.get_profile(user_id))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/profile/<user_id>', methods=['PUT'])
def update_profile(user_id):
    """Update user profile"""
    try:
        data = request.get_json()
        result = asyncio.run(supabase_service.update_profile(user_id, data))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
