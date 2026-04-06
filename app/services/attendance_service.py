from app.services import get_supabase
from app.services.email_service import send_absence_notification, send_low_attendance_alert
from datetime import date as date_type, datetime


def mark_attendance(class_id: str, subject_id: str, date: str, records: list, marked_by: str) -> dict:
    """
    Mark attendance for a class. Records = [{student_id, status}]
    After marking, auto-sends emails for absent students.
    """
    try:
        sb = get_supabase()

        # Build attendance rows
        rows = []
        for record in records:
            rows.append({
                "student_id": record["student_id"],
                "subject_id": subject_id,
                "classroom_id": class_id,
                "date": date,
                "status": record["status"],  # P, A, or L
                "marked_by": marked_by,
            })

        # Upsert attendance (update if same student+subject+date exists)
        result = sb.table("attendance").upsert(
            rows,
            on_conflict="student_id,subject_id,date"
        ).execute()

        # Get absent students and send emails
        absent_students = [r for r in records if r["status"] == "A"]
        emails_sent = 0

        if absent_students:
            # Get student profiles with parent emails
            absent_ids = [s["student_id"] for s in absent_students]
            profiles = sb.table("profiles").select(
                "id, full_name, parent_email"
            ).in_("id", absent_ids).execute()

            # Get subject name
            subject = sb.table("subjects").select("name").eq("id", subject_id).single().execute()
            subject_name = subject.data["name"] if subject.data else "Unknown Subject"

            for profile in profiles.data or []:
                parent_email = profile.get("parent_email")
                if parent_email:
                    send_absence_notification(
                        parent_email=parent_email,
                        student_name=profile["full_name"],
                        subject_name=subject_name,
                        date=date,
                    )
                    emails_sent += 1

                    # Check if attendance dropped below 75%
                    att_stats = get_student_subject_attendance(profile["id"], subject_id)
                    if att_stats and att_stats["percentage"] < 75.0:
                        send_low_attendance_alert(
                            parent_email=parent_email,
                            student_name=profile["full_name"],
                            percentage=att_stats["percentage"],
                            subject_name=subject_name,
                        )

            # Log emails
            if emails_sent > 0:
                sb.table("email_logs").insert({
                    "type": "absence_notification",
                    "recipient_count": emails_sent,
                    "subject_id": subject_id,
                    "date": date,
                    "sent_by": marked_by,
                }).execute()

        return {
            "success": True,
            "total_marked": len(records),
            "present": len([r for r in records if r["status"] == "P"]),
            "absent": len(absent_students),
            "emails_sent": emails_sent,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_student_subject_attendance(student_id: str, subject_id: str) -> dict:
    """Get attendance stats for a student in a specific subject."""
    try:
        sb = get_supabase()
        records = sb.table("attendance").select("status").eq(
            "student_id", student_id
        ).eq("subject_id", subject_id).execute()

        if not records.data:
            return None

        total = len(records.data)
        present = sum(1 for r in records.data if r["status"] == "P")
        percentage = (present / total * 100) if total > 0 else 0

        return {
            "total": total,
            "present": present,
            "absent": total - present,
            "percentage": round(percentage, 1),
        }
    except Exception:
        return None


def get_student_attendance(student_id: str) -> dict:
    """Get full attendance overview for a student across all subjects."""
    try:
        sb = get_supabase()
        records = sb.table("attendance").select(
            "*, subjects(name, code)"
        ).eq("student_id", student_id).order("date", desc=True).execute()

        if not records.data:
            return {"subjects": [], "overall_percentage": 0, "records": []}

        # Group by subject
        by_subject = {}
        for r in records.data:
            subj = r.get("subjects", {})
            subj_name = subj.get("name", "Unknown") if subj else "Unknown"
            subj_code = subj.get("code", "") if subj else ""
            sid = r["subject_id"]

            if sid not in by_subject:
                by_subject[sid] = {
                    "subject_id": sid,
                    "subject_name": subj_name,
                    "subject_code": subj_code,
                    "total": 0,
                    "present": 0,
                }
            by_subject[sid]["total"] += 1
            if r["status"] == "P":
                by_subject[sid]["present"] += 1

        subjects = []
        for sid, data in by_subject.items():
            data["percentage"] = round(data["present"] / data["total"] * 100, 1) if data["total"] > 0 else 0
            subjects.append(data)

        total_all = sum(s["total"] for s in subjects)
        present_all = sum(s["present"] for s in subjects)
        overall = round(present_all / total_all * 100, 1) if total_all > 0 else 0

        return {
            "subjects": subjects,
            "overall_percentage": overall,
            "total_lectures": total_all,
            "total_present": present_all,
            "records": records.data[:50],  # last 50 records
        }
    except Exception as e:
        return {"subjects": [], "overall_percentage": 0, "records": [], "error": str(e)}


def get_class_attendance(class_id: str, subject_id: str, date: str) -> list:
    """Get attendance for a specific class on a specific date."""
    try:
        sb = get_supabase()
        records = sb.table("attendance").select(
            "*, profiles(full_name, roll_number)"
        ).eq("classroom_id", class_id).eq(
            "subject_id", subject_id
        ).eq("date", date).execute()
        return records.data or []
    except Exception:
        return []


def get_teacher_attendance_history(teacher_id: str, limit: int = 20) -> list:
    """Get recent attendance records marked by a teacher."""
    try:
        sb = get_supabase()
        records = sb.table("attendance").select(
            "date, status, subject_id, classroom_id, subjects(name)"
        ).eq("marked_by", teacher_id).order(
            "date", desc=True
        ).limit(limit).execute()
        return records.data or []
    except Exception:
        return []
