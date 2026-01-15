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
