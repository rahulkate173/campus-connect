from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from app.services.auth_service import require_role, get_current_user
from app.services.academic_service import (
    get_student_marks, get_student_results, get_student_fees,
    get_parent_dashboard_stats, get_profile,
)
from app.services.attendance_service import get_student_attendance
from app.services.announcement_service import get_announcements
from app.services import get_supabase

parents_bp = Blueprint("parents", __name__)


def _get_ward(user):
    """Get the student ward linked to this parent."""
    try:
        sb = get_supabase()
        ward = sb.table("profiles").select("*").eq(
            "parent_email", user["email"]
        ).eq("role", "student").execute()
        return ward.data[0] if ward.data else None
    except Exception:
        return None


@parents_bp.route("/")
@require_role("parent")
def dashboard():
    user = get_current_user()
    stats = get_parent_dashboard_stats(user["email"])
    return render_template("parent/dashboard.html", user=user, stats=stats)


@parents_bp.route("/attendance")
@require_role("parent")
def attendance():
    user = get_current_user()
    ward = _get_ward(user)
    att_data = {}
    if ward:
        att_data = get_student_attendance(ward["id"])
    return render_template("parent/attendance.html", user=user, ward=ward, attendance=att_data)


@parents_bp.route("/academics")
@require_role("parent")
def academics():
    user = get_current_user()
    ward = _get_ward(user)
    marks_data = []
    results_data = []
    if ward:
        marks_data = get_student_marks(ward["id"])
        results_data = get_student_results(ward["id"])
    return render_template("parent/academics.html", user=user, ward=ward,
                           marks=marks_data, results=results_data)


@parents_bp.route("/announcements")
@require_role("parent")
def announcements():
    user = get_current_user()
    ann_data = get_announcements(role="parent")
    return render_template("parent/announcements.html", user=user, announcements=ann_data)


@parents_bp.route("/fees")
@require_role("parent")
def fees():
    user = get_current_user()
    ward = _get_ward(user)
    fees_data = []
    if ward:
        fees_data = get_student_fees(ward["id"])
    return render_template("parent/fees.html", user=user, ward=ward, fees=fees_data)


@parents_bp.route("/teachers")
@require_role("parent")
def teachers_directory():
    """View ward's teachers."""
    user = get_current_user()
    ward = _get_ward(user)
    teachers = []
    if ward and ward.get("classroom_id"):
        try:
            sb = get_supabase()
            subjects = sb.table("subjects").select(
                "name, profiles!subjects_teacher_id_fkey(full_name, email, department)"
            ).eq("classroom_id", ward["classroom_id"]).execute()
            teachers = subjects.data or []
        except Exception:
            pass
    return render_template("parent/teachers.html", user=user, ward=ward, teachers=teachers)


# Backward compatibility
@parents_bp.route("/login")
def login():
    return redirect(url_for("auth.login_page", role="parent"))
