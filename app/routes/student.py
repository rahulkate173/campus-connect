"""
Student portal routes for Campus Connect
"""
from flask import Blueprint, request, jsonify, render_template
from app.services.supabase_service import SupabaseService
import asyncio

bp = Blueprint('student', __name__)
supabase_service = SupabaseService()

# Page routes
@bp.route('/dashboard')
def dashboard():
    """Render student dashboard"""
    return render_template('student-dashboard.html')

@bp.route('/classroom')
def classroom():
    """Render classroom page"""
    return render_template('classroom.html')

@bp.route('/timetable')
def timetable():
    """Render timetable page"""
    return render_template('timetable.html')

@bp.route('/assignment')
def assignment():
    """Render assignment page"""
    return render_template('assignment.html')

@bp.route('/announcement')
def announcement():
    """Render announcement page"""
    return render_template('announcement.html')

@bp.route('/online-test')
def online_test():
    """Render online test page"""
    return render_template('online-test.html')

@bp.route('/attendance')
def attendance():
    """Render attendance page"""
    return render_template('attendence.html')

@bp.route('/examination')
def examination():
    """Render examination page"""
    return render_template('examination.html')

@bp.route('/exam-timetable')
def exam_timetable():
    """Render exam timetable page"""
    return render_template('examTimetable.html')

@bp.route('/internal-marks')
def internal_marks():
    """Render internal marks page"""
    return render_template('internal-marks.html')

@bp.route('/results')
def results():
    """Render results page"""
    return render_template('results.html')

@bp.route('/career')
def career():
    """Render career page"""
    return render_template('career.html')

@bp.route('/certificate')
def certificate():
    """Render certificate page"""
    return render_template('certificate.html')

@bp.route('/hackathon')
def hackathon():
    """Render hackathon page"""
    return render_template('hackathon.html')

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

@bp.route('/api/announcements')
def get_announcements():
    """Get announcements for students"""
    try:
        role = request.args.get('role', 'student')
        result = asyncio.run(supabase_service.get_announcements(role))
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
