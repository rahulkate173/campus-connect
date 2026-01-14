try:
    from supabase import create_client
except Exception as e:
    create_client = None
    _import_error = e

from .config import Config


_supabase = None
_supabase_error = None


def get_supabase():
    global _supabase
    global _supabase_error
    if create_client is None:
        if _supabase_error is None:
            _supabase_error = _import_error
        raise RuntimeError("Supabase client not available: %s" % _supabase_error)
    if _supabase is None and _supabase_error is None:
        try:
            _supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_ANON_KEY)
        except Exception as e:
            _supabase_error = e
            raise RuntimeError("Supabase init error: %s" % e)
    if _supabase_error is not None:
        raise RuntimeError("Supabase init error: %s" % _supabase_error)
    return _supabase


def supabase_available():
    return _supabase is not None and _supabase_error is None


def get_supabase_error():
    return _supabase_error


def create_user(email: str, password: str, role: str, full_name: str = ""):
    supabase = get_supabase()
    # Create auth user
    try:
        supabase.auth.sign_up({"email": email, "password": password})
    except Exception:
        # ignore if already exists for demo purposes
        pass

    # Ensure profile row
    profile = {"email": email, "role": role, "full_name": full_name}
    supabase.table("profiles").upsert(profile, on_conflict=["email"]).execute()


def get_profile_by_email(email: str):
    supabase = get_supabase()
    resp = supabase.table("profiles").select("*").eq("email", email).limit(1).execute()
    data = getattr(resp, "data", None)
    if data:
        return data[0]
    return None


def get_profile_by_id(user_id: str):
    supabase = get_supabase()
    resp = supabase.table("profiles").select("*").eq("id", user_id).limit(1).execute()
    data = getattr(resp, "data", None)
    if data:
        return data[0]
    return None


def verify_user(email: str, password: str):
    supabase = get_supabase()
    # Use Supabase auth to sign in
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = getattr(res, "user", None)
        if user:
            profile = get_profile_by_email(email)
            return profile
    except Exception:
        return None
    return None
