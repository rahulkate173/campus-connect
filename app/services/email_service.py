import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
COLLEGE_NAME = os.getenv("COLLEGE_NAME", "Campus Connect")


def send_absence_notification(parent_email: str, student_name: str, subject_name: str, date: str) -> dict:
    """Send email to parent when student is marked absent."""
    try:
        html_content = f"""
        <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a1a; color: #e0e0e0; border-radius: 16px; overflow: hidden;">
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 24px;">🎓 {COLLEGE_NAME}</h1>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0;">Campus Connect — Attendance Alert</p>
            </div>
            <div style="padding: 30px;">
                <h2 style="color: #ff6b6b; margin-top: 0;">⚠️ Absence Notification</h2>
                <p>Dear Parent,</p>
                <p>This is to inform you that your ward <strong style="color: #667eea;">{student_name}</strong> was marked <strong style="color: #ff6b6b;">ABSENT</strong> in the following lecture:</p>
                <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; margin: 20px 0; border-left: 4px solid #ff6b6b;">
                    <p style="margin: 5px 0;"><strong>Subject:</strong> {subject_name}</p>
                    <p style="margin: 5px 0;"><strong>Date:</strong> {date}</p>
                </div>
                <p>If you believe this is an error, please contact the respective faculty member.</p>
                <p style="color: #888; font-size: 14px; margin-top: 30px;">— {COLLEGE_NAME} Administration</p>
            </div>
        </div>
        """
        params = {
            "from": f"{COLLEGE_NAME} <onboarding@resend.dev>",
            "to": [parent_email],
            "subject": f"Absence Alert: {student_name} — {subject_name} ({date})",
            "html": html_content,
        }
        email = resend.Emails.send(params)
        return {"success": True, "email_id": email.get("id")}
    except Exception as e:
        print(f"Email send error: {e}")
        return {"success": False, "error": str(e)}


def send_low_attendance_alert(parent_email: str, student_name: str, percentage: float, subject_name: str) -> dict:
    """Send alert when student attendance drops below 75%."""
    try:
        html_content = f"""
        <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a1a; color: #e0e0e0; border-radius: 16px; overflow: hidden;">
            <div style="background: linear-gradient(135deg, #f093fb, #f5576c); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 24px;">🎓 {COLLEGE_NAME}</h1>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0;">Campus Connect — Low Attendance Warning</p>
            </div>
            <div style="padding: 30px;">
                <h2 style="color: #f5576c; margin-top: 0;">🚨 Low Attendance Warning</h2>
                <p>Dear Parent,</p>
                <p>Your ward <strong style="color: #667eea;">{student_name}</strong>'s attendance in <strong>{subject_name}</strong> has dropped to a critical level.</p>
                <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; border: 2px solid #f5576c;">
                    <p style="font-size: 48px; font-weight: bold; color: #f5576c; margin: 0;">{percentage:.1f}%</p>
                    <p style="color: #888; margin: 5px 0;">Current Attendance</p>
                    <p style="color: #ff6b6b; font-size: 14px;">Minimum required: 75%</p>
                </div>
                <p>Please ensure regular attendance to avoid academic penalties.</p>
                <p style="color: #888; font-size: 14px; margin-top: 30px;">— {COLLEGE_NAME} Administration</p>
            </div>
        </div>
        """
        params = {
            "from": f"{COLLEGE_NAME} <onboarding@resend.dev>",
            "to": [parent_email],
            "subject": f"⚠️ Low Attendance Alert: {student_name} — {percentage:.1f}% in {subject_name}",
            "html": html_content,
        }
        email = resend.Emails.send(params)
        return {"success": True, "email_id": email.get("id")}
    except Exception as e:
        print(f"Email send error: {e}")
        return {"success": False, "error": str(e)}


def send_announcement_email(recipients: list, title: str, body: str, sender_name: str) -> dict:
    """Send announcement notification to a list of recipients."""
    try:
        html_content = f"""
        <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a1a; color: #e0e0e0; border-radius: 16px; overflow: hidden;">
            <div style="background: linear-gradient(135deg, #00b09b, #96c93d); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 24px;">🎓 {COLLEGE_NAME}</h1>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0;">Campus Connect — New Announcement</p>
            </div>
            <div style="padding: 30px;">
                <h2 style="color: #00b09b; margin-top: 0;">📢 {title}</h2>
                <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; margin: 20px 0;">
                    <p>{body}</p>
                </div>
                <p style="color: #888; font-size: 14px;">Posted by: {sender_name}</p>
                <p style="color: #888; font-size: 14px; margin-top: 30px;">— {COLLEGE_NAME} Administration</p>
            </div>
        </div>
        """
        # Send to each recipient (Resend supports batch)
        for recipient in recipients[:100]:  # limit to 100 per batch
            params = {
                "from": f"{COLLEGE_NAME} <onboarding@resend.dev>",
                "to": [recipient],
                "subject": f"📢 {title} — {COLLEGE_NAME}",
                "html": html_content,
            }
            resend.Emails.send(params)
        return {"success": True, "sent_count": min(len(recipients), 100)}
    except Exception as e:
        print(f"Announcement email error: {e}")
        return {"success": False, "error": str(e)}
