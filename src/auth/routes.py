from flask import render_template, redirect, url_for, flash, request, session
from flask import current_app as app
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from . import bp
from .forms import SignupForm, LoginForm
from ..models import create_user, get_profile_by_email, verify_user


login_manager = LoginManager()


class User(UserMixin):
    def __init__(self, id, email, role=None, full_name=None):
        self.id = str(id)
        self.email = email
        self.role = role
        self.full_name = full_name


@login_manager.user_loader
def load_user(user_id):
    profile = get_profile_by_id_safe(user_id)
    if profile:
        return User(profile.get("id"), profile.get("email"), profile.get("role"), profile.get("full_name"))
    return None


def get_profile_by_id_safe(user_id):
    # helper - profiles can be referenced by id or email
    try:
        from ..models import get_profile_by_id

        return get_profile_by_id(user_id)
    except Exception:
        return None


@bp.record_once
def on_load(state):
    app = state.app
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        create_user(form.email.data, form.password.data, form.role.data, form.full_name.data)
        flash("Signup successful. Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/signup.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        profile = verify_user(form.email.data, form.password.data)
        if profile:
            user = User(profile.get("id", profile.get("email")), profile.get("email"), profile.get("role"), profile.get("full_name"))
            login_user(user)
            flash("Logged in successfully.", "success")
            role = user.role or "student"
            if role == "teacher":
                return redirect(url_for("teacher.dashboard"))
            if role == "parent":
                return redirect(url_for("parent.dashboard"))
            return redirect(url_for("student.dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("auth.login"))
