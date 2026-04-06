from functools import wraps
from flask import session, redirect, url_for, flash, request
from app.services import get_supabase, get_supabase_admin
import os


def signup_user(email: str, password: str, role: str, profile_data: dict) -> dict:
    """Register a new user with Supabase Auth and create profile."""
    try:
        sb = get_supabase()
        # Sign up via Supabase Auth
        auth_response = sb.auth.sign_up({
            "email": email,
            "password": password,
        })

        if auth_response.user:
            user_id = auth_response.user.id
            # Create profile record
            profile = {
                "id": user_id,
                "email": email,
                "role": role,
                "full_name": profile_data.get("full_name", ""),
                "department": profile_data.get("department", ""),
                "year": profile_data.get("year", ""),
                "division": profile_data.get("division", ""),
                "roll_number": profile_data.get("roll_number", ""),
                "parent_email": profile_data.get("parent_email", ""),
                "phone": profile_data.get("phone", ""),
            }
            sb.table("profiles").insert(profile).execute()
            return {"success": True, "user_id": user_id}
        return {"success": False, "error": "Signup failed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def login_user(email: str, password: str) -> dict:
    """Authenticate user and return session data."""
    try:
        sb = get_supabase()
        auth_response = sb.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })

        if auth_response.user:
            user_id = auth_response.user.id
            # Fetch profile
            profile = sb.table("profiles").select("*").eq("id", user_id).single().execute()
            if profile.data:
                return {
                    "success": True,
                    "user": {
                        "id": user_id,
                        "email": email,
                        "role": profile.data["role"],
                        "full_name": profile.data["full_name"],
                        "department": profile.data.get("department", ""),
                        "year": profile.data.get("year", ""),
                        "division": profile.data.get("division", ""),
                        "roll_number": profile.data.get("roll_number", ""),
                        "parent_email": profile.data.get("parent_email", ""),
                        "phone": profile.data.get("phone", ""),
                    },
                    "access_token": auth_response.session.access_token,
                }
        return {"success": False, "error": "Invalid email or password"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_current_user() -> dict:
    """Get current user from Flask session."""
    user = session.get("user")
    if not user:
        return None
    return user


def require_role(*roles):
    """Decorator to require specific role(s) for a route."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("auth.login_page"))
            if user.get("role") not in roles:
                flash("You don't have permission to access this page.", "danger")
                return redirect(url_for("index"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def logout_user():
    """Clear session and sign out."""
    try:
        sb = get_supabase()
        sb.auth.sign_out()
    except Exception:
        pass
    session.clear()
