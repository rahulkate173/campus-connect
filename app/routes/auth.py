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

# Classroom API routes (shared across portals)
@bp.route('/api/classrooms')
def get_classrooms():
    """Get all classrooms"""
    try:
        result = asyncio.run(supabase_service.get_all_classrooms())
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/classroom/<class_year>')
def get_classroom(class_year):
    """Get classroom by year"""
    try:
        result = asyncio.run(supabase_service.get_classroom_by_year(class_year))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/classroom/<class_year>/timetable')
def get_classroom_timetable(class_year):
    """Get classroom timetable"""
    try:
        result = asyncio.run(supabase_service.get_timetable(class_year))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/classroom/<class_year>/timetable', methods=['PUT'])
def update_timetable(class_year):
    """Update classroom timetable"""
    try:
        data = request.get_json()
        timetable = data.get('timetable', {})
        result = asyncio.run(supabase_service.update_timetable(class_year, timetable))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Attendance API routes
@bp.route('/api/attendance/<student_id>')
def get_attendance(student_id):
    """Get student attendance"""
    try:
        result = asyncio.run(supabase_service.get_student_attendance(student_id))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/attendance', methods=['POST'])
def create_attendance_record():
    """Create attendance record"""
    try:
        data = request.get_json()
        result = asyncio.run(supabase_service.create_attendance(data))
        if result.get('success'):
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/attendance/<attendance_id>', methods=['PUT'])
def update_attendance_record(attendance_id):
    """Update attendance record"""
    try:
        data = request.get_json()
        result = asyncio.run(supabase_service.update_attendance(attendance_id, data))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Assignment API routes
@bp.route('/api/assignments/<classroom_id>')
def get_assignments(classroom_id):
    """Get assignments for classroom"""
    try:
        result = asyncio.run(supabase_service.get_assignments(classroom_id))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/assignments', methods=['POST'])
def create_assignment():
    """Create assignment"""
    try:
        data = request.get_json()
        result = asyncio.run(supabase_service.create_assignment(data))
        if result.get('success'):
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/assignments/<assignment_id>', methods=['PUT'])
def update_assignment(assignment_id):
    """Update assignment"""
    try:
        data = request.get_json()
        result = asyncio.run(supabase_service.update_assignment(assignment_id, data))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/assignments/<assignment_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    """Delete assignment"""
    try:
        result = asyncio.run(supabase_service.delete_assignment(assignment_id))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Marks API routes
@bp.route('/api/marks/<student_id>')
def get_marks(student_id):
    """Get student marks"""
    try:
        result = asyncio.run(supabase_service.get_student_marks(student_id))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/marks', methods=['POST'])
def create_marks():
    """Create marks record"""
    try:
        data = request.get_json()
        result = asyncio.run(supabase_service.create_marks(data))
        if result.get('success'):
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/marks/<mark_id>', methods=['PUT'])
def update_marks(mark_id):
    """Update marks record"""
    try:
        data = request.get_json()
        result = asyncio.run(supabase_service.update_marks(mark_id, data))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Announcement API routes
@bp.route('/api/announcements')
def get_announcements():
    """Get announcements with optional role filter"""
    try:
        role = request.args.get('role')
        result = asyncio.run(supabase_service.get_announcements(role))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/announcements', methods=['POST'])
def create_announcement_api():
    """Create announcement"""
    try:
        data = request.get_json()
        result = asyncio.run(supabase_service.create_announcement(data))
        if result.get('success'):
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/announcements/<announcement_id>', methods=['DELETE'])
def delete_announcement(announcement_id):
    """Delete announcement"""
    try:
        result = asyncio.run(supabase_service.delete_announcement(announcement_id))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Student and Parent API routes
@bp.route('/api/students/<class_year>')
def get_students(class_year):
    """Get students by class year"""
    try:
        result = asyncio.run(supabase_service.get_students_by_class(class_year))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/parent/<parent_id>/child')
def get_parent_child_info(parent_id):
    """Get parent's child information"""
    try:
        result = asyncio.run(supabase_service.get_parent_child_info(parent_id))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
