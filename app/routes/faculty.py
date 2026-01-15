"""
Faculty portal routes for Campus Connect
"""
from flask import Blueprint, request, jsonify, render_template
from app.services.supabase_service import SupabaseService
import asyncio

bp = Blueprint('faculty', __name__)
supabase_service = SupabaseService()

# Page routes
@bp.route('/dashboard')
def dashboard():
    """Render faculty dashboard"""
    return render_template('facultydashboard.html')

@bp.route('/classroom')
def classroom():
    """Render faculty classroom page"""
    return render_template('faculty-class.html')

@bp.route('/timetable')
def timetable():
    """Render faculty timetable page"""
    return render_template('faculty-time-table.html')

@bp.route('/mark-attendance')
def mark_attendance():
    """Render mark attendance page"""
    return render_template('markAttendence.html')

@bp.route('/create-attendance')
def create_attendance():
    """Render create attendance page"""
    return render_template('create-attendence.html')

@bp.route('/create-test')
def create_test():
    """Render create test page"""
    return render_template('create-test.html')

@bp.route('/create-announcement')
def create_announcement():
    """Render create announcement page"""
    return render_template('create-announcement.html')

@bp.route('/manage-assignment')
def manage_assignment():
    """Render manage assignment page"""
    return render_template('manage-assignment.html')

@bp.route('/examhub')
def examhub():
    """Render exam hub page"""
    return render_template('facultyExamhub.html')

@bp.route('/create-exam-timetable')
def create_exam_timetable():
    """Render create exam timetable page"""
    return render_template('create-exam-timetable.html')

@bp.route('/create-internal-marks')
def create_internal_marks():
    """Render create internal marks page"""
    return render_template('create-internal-marks.html')

@bp.route('/create-result')
def create_result():
    """Render create result page"""
    return render_template('create-result.html')

# API routes
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
