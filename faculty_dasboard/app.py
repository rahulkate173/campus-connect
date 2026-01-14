import csv
import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__, template_folder='templates')
app.secret_key = 'dev-secret-change-this'

USERS_CSV = os.path.join(DATA_DIR, 'users.csv')

BRANCHES = ['FE', 'SE', 'TE', 'BE']

# --- CSV utilities ---

def ensure_csv(path, headers):
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def append_csv(path, row, headers=None):
    create = not os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers or row.keys())
        if create:
            writer.writeheader()
        writer.writerow(row)


def overwrite_csv(path, rows, headers):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

# --- User utilities ---

def find_user_by_email(email):
    users = read_csv(USERS_CSV)
    for u in users:
        if u['email'] == email:
            return u
    return None

# ensure users csv exists
ensure_csv(USERS_CSV, ['id', 'name', 'email', 'password'])

# --- Routes ---

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('select_branch'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if find_user_by_email(email):
            flash('Email already exists')
            return redirect(url_for('signup'))
        uid = str(uuid.uuid4())
        append_csv(USERS_CSV, {'id': uid, 'name': name, 'email': email, 'password': password}, headers=['id','name','email','password'])
        session['user'] = {'id': uid, 'name': name, 'email': email}
        return redirect(url_for('select_branch'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = find_user_by_email(email)
        if user and user['password'] == password:
            session['user'] = {'id': user['id'], 'name': user['name'], 'email': user['email']}
            return redirect(url_for('select_branch'))
        flash('Invalid credentials')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/select-branch', methods=['GET', 'POST'])
def select_branch():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        branch = request.form['branch']
        if branch not in BRANCHES:
            flash('Invalid branch')
            return redirect(url_for('select_branch'))
        session['branch'] = branch
        return redirect(url_for('dashboard'))
    return render_template('select_branch.html', branches=BRANCHES)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session or 'branch' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', branch=session['branch'])

# --- Classroom Routes ---

def branch_path(kind, branch):
    return os.path.join(DATA_DIR, f"{kind}_{branch}.csv")

@app.route('/classroom/timetable', methods=['GET', 'POST'])
def timetable():
    branch = session.get('branch')
    if not branch:
        return redirect(url_for('select_branch'))
    path = branch_path('timetable', branch)
    headers = ['id', 'day', 'start', 'end', 'subject', 'note']
    ensure_csv(path, headers)
    if request.method == 'POST':
        row = {
            'id': str(uuid.uuid4()),
            'day': request.form['day'],
            'start': request.form['start'],
            'end': request.form['end'],
            'subject': request.form['subject'],
            'note': request.form.get('note', '')
        }
        append_csv(path, row, headers=headers)
        return redirect(url_for('timetable'))
    rows = read_csv(path)
    return render_template('timetable.html', rows=rows, branch=branch)

@app.route('/classroom/assignments', methods=['GET', 'POST'])
def assignments():
    branch = session.get('branch')
    path = branch_path('assignments', branch)
    headers = ['id', 'title', 'description', 'deadline', 'created_at']
    ensure_csv(path, headers)
    if request.method == 'POST':
        row = {
            'id': str(uuid.uuid4()),
            'title': request.form['title'],
            'description': request.form.get('description',''),
            'deadline': request.form.get('deadline',''),
            'created_at': datetime.utcnow().isoformat()
        }
        append_csv(path, row, headers=headers)
        return redirect(url_for('assignments'))
    rows = read_csv(path)
    return render_template('assignments.html', rows=rows, branch=branch)

@app.route('/classroom/online-tests', methods=['GET', 'POST'])
def online_tests():
    branch = session.get('branch')
    path = branch_path('tests', branch)
    headers = ['id', 'title', 'form_url', 'scores_file']
    ensure_csv(path, headers)
    if request.method == 'POST':
        title = request.form['title']
        form_url = request.form.get('form_url', '')
        file = request.files.get('scores_file')
        tid = str(uuid.uuid4())
        scores_file = ''
        if file and file.filename:
            scores_path = os.path.join(DATA_DIR, f"scores_{tid}.csv")
            file.save(scores_path)
            scores_file = os.path.basename(scores_path)
        row = {'id': tid, 'title': title, 'form_url': form_url, 'scores_file': scores_file}
        append_csv(path, row, headers=headers)
        return redirect(url_for('online_tests'))
    rows = read_csv(path)
    return render_template('online_tests.html', rows=rows, branch=branch)

@app.route('/scores/<filename>')
def scores_file(filename):
    return send_from_directory(DATA_DIR, filename)

@app.route('/classroom/attendance', methods=['GET', 'POST'])
def attendance():
    branch = session.get('branch')
    path = branch_path('attendance', branch)
    headers = ['id', 'date', 'student_id', 'status']
    ensure_csv(path, headers)
    if request.method == 'POST':
        date = request.form.get('date')
        entries = request.form.get('entries')  # expects lines: student_id,status
        for line in entries.splitlines():
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 2:
                continue
            row = {'id': str(uuid.uuid4()), 'date': date, 'student_id': parts[0], 'status': parts[1]}
            append_csv(path, row, headers=headers)
        return redirect(url_for('attendance'))
    rows = read_csv(path)
    return render_template('attendance.html', rows=rows, branch=branch)

@app.route('/classroom/attendance/analysis')
def attendance_analysis():
    branch = session.get('branch')
    path = branch_path('attendance', branch)
    rows = read_csv(path)
    # simple aggregation per student
    stats = {}
    for r in rows:
        sid = r['student_id']
        stats.setdefault(sid, {'present':0, 'absent':0})
        if r['status'].lower() in ('present','p','yes','1'):
            stats[sid]['present'] += 1
        else:
            stats[sid]['absent'] += 1
    return render_template('attendance_analysis.html', stats=stats, branch=branch)

# --- Examination area ---
@app.route('/examination')
def examination():
    branch = session.get('branch')
    return render_template('examination.html', branch=branch)

# --- Run ---
if __name__ == '__main__':
    app.run(debug=True)
