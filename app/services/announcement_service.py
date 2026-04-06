from app.services import get_supabase
from app.services.email_service import send_announcement_email


def create_announcement(title: str, body: str, target_role: str, classroom_id: str, created_by: str) -> dict:
    """Create a new announcement."""
    try:
        sb = get_supabase()
        data = {
            "title": title,
            "body": body,
            "target_role": target_role,  # 'all', 'student', 'teacher', 'parent'
            "created_by": created_by,
        }
        if classroom_id:
            data["classroom_id"] = classroom_id

        result = sb.table("announcements").insert(data).execute()

        # Optionally send email notification
        if target_role in ("all", "parent"):
            # Get parent emails
            parents = sb.table("profiles").select("email").eq("role", "parent").execute()
            if parents.data:
                emails = [p["email"] for p in parents.data if p.get("email")]
                creator = sb.table("profiles").select("full_name").eq("id", created_by).single().execute()
                sender_name = creator.data.get("full_name", "Faculty") if creator.data else "Faculty"
                send_announcement_email(emails, title, body, sender_name)

        return {"success": True, "id": result.data[0]["id"] if result.data else None}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_announcements(role: str = None, classroom_id: str = None, limit: int = 20) -> list:
    """Get announcements filtered by role and/or classroom."""
    try:
        sb = get_supabase()
        query = sb.table("announcements").select(
            "*, profiles!announcements_created_by_fkey(full_name)"
        )
        if role and role != "all":
            query = query.in_("target_role", [role, "all"])
        if classroom_id:
            query = query.or_(f"classroom_id.eq.{classroom_id},classroom_id.is.null")
        result = query.order("created_at", desc=True).limit(limit).execute()
        return result.data or []
    except Exception:
        return []


def delete_announcement(announcement_id: str, user_id: str) -> dict:
    """Delete an announcement (only creator can delete)."""
    try:
        sb = get_supabase()
        sb.table("announcements").delete().eq(
            "id", announcement_id
        ).eq("created_by", user_id).execute()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
