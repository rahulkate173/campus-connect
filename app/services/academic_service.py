from app.services import get_supabase


# ── Marks ──────────────────────────────────────────────────
def get_student_marks(student_id: str, semester: int = None) -> list:
    """Get marks for a student, optionally filtered by semester."""
    try:
        sb = get_supabase()
        query = sb.table("marks").select(
            "*, subjects(name, code, credits)"
        ).eq("student_id", student_id)
        if semester:
            query = query.eq("semester", semester)
        result = query.order("created_at", desc=True).execute()
        return result.data or []
    except Exception:
        return []


def enter_marks(marks_list: list) -> dict:
    """Enter marks for multiple students. marks_list = [{student_id, subject_id, exam_type, marks_obtained, max_marks, semester}]"""
    try:
        sb = get_supabase()
        result = sb.table("marks").upsert(
            marks_list,
            on_conflict="student_id,subject_id,exam_type"
        ).execute()
        return {"success": True, "count": len(marks_list)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_class_marks(class_id: str, subject_id: str, exam_type: str) -> list:
    """Get marks for all students in a class for a specific exam."""
    try:
        sb = get_supabase()
        # Get students in class
        students = sb.table("profiles").select("id, full_name, roll_number").eq(
            "classroom_id", class_id
        ).eq("role", "student").order("roll_number").execute()

        marks = sb.table("marks").select("*").eq(
            "subject_id", subject_id
        ).eq("exam_type", exam_type).execute()

        marks_map = {m["student_id"]: m for m in (marks.data or [])}

        result = []
        for s in students.data or []:
            m = marks_map.get(s["id"], {})
            result.append({
                "student_id": s["id"],
                "full_name": s["full_name"],
                "roll_number": s["roll_number"],
                "marks_obtained": m.get("marks_obtained", None),
                "max_marks": m.get("max_marks", None),
            })
        return result
    except Exception:
        return []


# ── Results ────────────────────────────────────────────────
def get_student_results(student_id: str) -> list:
    """Get semester results for a student."""
    try:
        sb = get_supabase()
        result = sb.table("results").select("*").eq(
            "student_id", student_id
        ).order("semester").execute()
        return result.data or []
    except Exception:
        return []


def upload_result(student_id: str, semester: int, sgpa: float, cgpa: float) -> dict:
    """Upload/update semester result for a student."""
    try:
        sb = get_supabase()
        sb.table("results").upsert({
            "student_id": student_id,
            "semester": semester,
            "sgpa": sgpa,
            "cgpa": cgpa,
        }, on_conflict="student_id,semester").execute()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── Assignments ────────────────────────────────────────────
def get_assignments(subject_id: str = None, class_id: str = None) -> list:
    """Get assignments filtered by subject or class."""
    try:
        sb = get_supabase()
        query = sb.table("assignments").select("*, subjects(name, code), profiles!assignments_created_by_fkey(full_name)")
        if subject_id:
            query = query.eq("subject_id", subject_id)
        if class_id:
            query = query.eq("classroom_id", class_id)
        result = query.order("due_date", desc=True).execute()
        return result.data or []
    except Exception:
        return []


def create_assignment(data: dict) -> dict:
    """Create a new assignment."""
    try:
        sb = get_supabase()
        result = sb.table("assignments").insert(data).execute()
        return {"success": True, "id": result.data[0]["id"] if result.data else None}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_student_submissions(student_id: str) -> list:
    """Get assignment submissions for a student."""
    try:
        sb = get_supabase()
        result = sb.table("assignment_submissions").select(
            "*, assignments(title, due_date, subject_id, subjects(name))"
        ).eq("student_id", student_id).order("submitted_at", desc=True).execute()
        return result.data or []
    except Exception:
        return []


def submit_assignment(student_id: str, assignment_id: str, file_url: str = None) -> dict:
    """Submit an assignment."""
    try:
        sb = get_supabase()
        sb.table("assignment_submissions").upsert({
            "student_id": student_id,
            "assignment_id": assignment_id,
            "file_url": file_url,
        }, on_conflict="student_id,assignment_id").execute()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── Timetable ─────────────────────────────────────────────
def get_timetable(class_id: str) -> list:
    """Get timetable for a class."""
    try:
        sb = get_supabase()
        result = sb.table("timetable").select(
            "*, subjects(name, code), profiles!timetable_teacher_id_fkey(full_name)"
        ).eq("classroom_id", class_id).order("day_of_week").order("start_time").execute()
        return result.data or []
    except Exception:
        return []


def get_teacher_timetable(teacher_id: str) -> list:
    """Get timetable for a teacher."""
    try:
        sb = get_supabase()
        result = sb.table("timetable").select(
            "*, subjects(name, code), classrooms(name, year, division)"
        ).eq("teacher_id", teacher_id).order("day_of_week").order("start_time").execute()
        return result.data or []
    except Exception:
        return []


# ── Subjects ──────────────────────────────────────────────
def get_subjects(class_id: str = None, teacher_id: str = None) -> list:
    """Get subjects filtered by class or teacher."""
    try:
        sb = get_supabase()
        query = sb.table("subjects").select("*")
        if class_id:
            query = query.eq("classroom_id", class_id)
        if teacher_id:
            query = query.eq("teacher_id", teacher_id)
        result = query.order("name").execute()
        return result.data or []
    except Exception:
        return []


# ── Classrooms ────────────────────────────────────────────
def get_classrooms(teacher_id: str = None) -> list:
    """Get classrooms, optionally filtered by teacher."""
    try:
        sb = get_supabase()
        if teacher_id:
            # Get classrooms where teacher has subjects
            subjects = sb.table("subjects").select("classroom_id").eq("teacher_id", teacher_id).execute()
            class_ids = list(set(s["classroom_id"] for s in (subjects.data or [])))
            if not class_ids:
                return []
            result = sb.table("classrooms").select("*").in_("id", class_ids).execute()
        else:
            result = sb.table("classrooms").select("*").execute()
        return result.data or []
    except Exception:
        return []


def get_students_in_class(class_id: str) -> list:
    """Get all students in a classroom."""
    try:
        sb = get_supabase()
        result = sb.table("profiles").select(
            "id, full_name, roll_number, email, parent_email"
        ).eq("classroom_id", class_id).eq(
            "role", "student"
        ).order("roll_number").execute()
        return result.data or []
    except Exception:
        return []


# ── Fees ──────────────────────────────────────────────────
def get_student_fees(student_id: str) -> list:
    """Get fee records for a student."""
    try:
        sb = get_supabase()
        result = sb.table("fees").select("*").eq(
            "student_id", student_id
        ).order("semester").execute()
        return result.data or []
    except Exception:
        return []


# ── Profile ───────────────────────────────────────────────
def get_profile(user_id: str) -> dict:
    """Get user profile."""
    try:
        sb = get_supabase()
        result = sb.table("profiles").select("*").eq("id", user_id).single().execute()
        return result.data
    except Exception:
        return None


def update_profile(user_id: str, data: dict) -> dict:
    """Update user profile."""
    try:
        sb = get_supabase()
        sb.table("profiles").update(data).eq("id", user_id).execute()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── Dashboard Stats ───────────────────────────────────────
def get_student_dashboard_stats(student_id: str) -> dict:
    """Get dashboard statistics for a student."""
    try:
        sb = get_supabase()
        # Attendance
        att = sb.table("attendance").select("status").eq("student_id", student_id).execute()
        total_att = len(att.data) if att.data else 0
        present = sum(1 for r in (att.data or []) if r["status"] == "P")
        att_pct = round(present / total_att * 100, 1) if total_att > 0 else 0

        # Pending assignments
        pending = sb.table("assignments").select("id").eq(
            "classroom_id",
            (sb.table("profiles").select("classroom_id").eq("id", student_id).single().execute()).data.get("classroom_id", "")
        ).execute()

        submitted = sb.table("assignment_submissions").select("assignment_id").eq(
            "student_id", student_id
        ).execute()
        submitted_ids = [s["assignment_id"] for s in (submitted.data or [])]
        pending_count = sum(1 for a in (pending.data or []) if a["id"] not in submitted_ids)

        # Announcements count
        announcements = sb.table("announcements").select("id", count="exact").execute()
        ann_count = announcements.count if announcements.count else 0

        return {
            "attendance_percentage": att_pct,
            "total_lectures": total_att,
            "lectures_attended": present,
            "pending_assignments": pending_count,
            "announcements": ann_count,
        }
    except Exception:
        return {
            "attendance_percentage": 0,
            "total_lectures": 0,
            "lectures_attended": 0,
            "pending_assignments": 0,
            "announcements": 0,
        }


def get_teacher_dashboard_stats(teacher_id: str) -> dict:
    """Get dashboard statistics for a teacher."""
    try:
        sb = get_supabase()
        classes = get_classrooms(teacher_id)
        subjects = get_subjects(teacher_id=teacher_id)

        # Total students across all classes
        total_students = 0
        for cls in classes:
            students = get_students_in_class(cls["id"])
            total_students += len(students)

        return {
            "total_classes": len(classes),
            "total_subjects": len(subjects),
            "total_students": total_students,
            "classes": classes,
            "subjects": subjects,
        }
    except Exception:
        return {
            "total_classes": 0,
            "total_subjects": 0,
            "total_students": 0,
            "classes": [],
            "subjects": [],
        }


def get_parent_dashboard_stats(parent_email: str) -> dict:
    """Get dashboard stats for a parent by looking up ward."""
    try:
        sb = get_supabase()
        # Find ward by parent_email
        ward = sb.table("profiles").select("*").eq(
            "parent_email", parent_email
        ).eq("role", "student").execute()

        if not ward.data:
            return {"ward": None}

        ward_data = ward.data[0]
        ward_id = ward_data["id"]

        # Get attendance stats
        from app.services.attendance_service import get_student_attendance
        attendance = get_student_attendance(ward_id)

        # Get recent announcements
        announcements = sb.table("announcements").select(
            "id", count="exact"
        ).execute()

        return {
            "ward": ward_data,
            "attendance": attendance,
            "announcements_count": announcements.count if announcements.count else 0,
        }
    except Exception:
        return {"ward": None}
