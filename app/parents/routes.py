from flask import Blueprint, render_template,session,redirect,request,url_for
import os
template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
parents_bp = Blueprint("parents", __name__,template_folder=template_path,static_folder=static_path)

@parents_bp.route("/")
def dashboard():
    return render_template("parentdashboard.html")

@parents_bp.route("/attendance")
def attendance():
    return render_template("parent-attendence.html")

@parents_bp.route("/academics")
def academics():
    return render_template("parentAcademics.html")

@parents_bp.route("/announcements")
def announcements():
    return render_template("parent-announcement.html")

@parents_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # TEMP authentication logic (replace with DB)
        if email.endswith('@gmail.com') and password == 'parent123':
            session['user_role'] = 'parent'
            session['parent_email'] = email

            return redirect(url_for('parents.dashboard'))

        return render_template(
            'parentlogin.html',
            error="Invalid email or password"
        )

    return render_template('parentLogin.html')



