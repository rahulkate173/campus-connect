# Campus Connect - College Management System

A comprehensive college management system with three portals: Student, Parent, and Teacher. Built with Flask/FastAPI backend and Supabase database, deployable on Vercel.

## Features

- **Student Portal**: Dashboard, attendance tracking, assignments, timetable, marks, announcements
- **Faculty Portal**: Classroom management, attendance marking, assignment creation, marks entry, announcements
- **Parent Portal**: View child's academics, attendance, and announcements
- **RESTful API**: Complete API for all operations
- **Supabase Integration**: Secure database with authentication
- **Vercel Deployment**: Serverless deployment ready
- **Docker Support**: Local development with Docker

## Tech Stack

- **Backend**: Flask + FastAPI
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Vercel (serverless)
- **Frontend**: HTML/CSS/JavaScript
- **Containerization**: Docker

## Setup

### Prerequisites

- Python 3.11+
- Supabase account and project
- Docker (optional, for containerized development)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rahulkate173/campus-connect.git
cd campus-connect
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

5. Run the application:
```bash
python app/main.py
```

The application will be available at `http://localhost:5000`

## Docker Setup

### Using Docker Compose (Recommended for Development)

```bash
# Build and run
docker-compose up

# Run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

### Using Docker

```bash
# Build the image
docker build -t campus-connect .

# Run the container
docker run -p 5000:5000 --env-file .env campus-connect
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
SECRET_KEY=your-secret-key-here
DEBUG=False
```

## API Documentation

### Authentication

- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Profiles

- `GET /api/profile/{user_id}` - Get user profile
- `PUT /api/profile/{user_id}` - Update user profile

### Classrooms

- `GET /api/classrooms` - Get all classrooms
- `GET /api/classroom/{class_year}` - Get classroom by year
- `GET /api/classroom/{class_year}/timetable` - Get timetable
- `PUT /api/classroom/{class_year}/timetable` - Update timetable

### Attendance

- `GET /api/attendance/{student_id}` - Get student attendance
- `POST /api/attendance` - Create attendance record
- `PUT /api/attendance/{attendance_id}` - Update attendance

### Assignments

- `GET /api/assignments/{classroom_id}` - Get assignments
- `POST /api/assignments` - Create assignment
- `PUT /api/assignments/{assignment_id}` - Update assignment
- `DELETE /api/assignments/{assignment_id}` - Delete assignment

### Marks

- `GET /api/marks/{student_id}` - Get student marks
- `POST /api/marks` - Create marks record
- `PUT /api/marks/{mark_id}` - Update marks

### Announcements

- `GET /api/announcements` - Get announcements (with optional `?role=` filter)
- `POST /api/announcements` - Create announcement
- `DELETE /api/announcements/{announcement_id}` - Delete announcement

### Students & Parents

- `GET /api/students/{class_year}` - Get students by class
- `GET /api/parent/{parent_id}/child` - Get parent's child info

## Deployment

### Vercel Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variables in Vercel dashboard:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SECRET_KEY`

## Project Structure

```
campus-connect/
├── api/
│   └── index.py           # FastAPI entry point for Vercel
├── app/
│   ├── __init__.py
│   ├── main.py            # Flask app factory
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py        # Authentication routes
│   │   ├── student.py     # Student routes
│   │   ├── faculty.py     # Faculty routes
│   │   └── parent.py      # Parent routes
│   ├── services/
│   │   ├── __init__.py
│   │   └── supabase_service.py  # Supabase operations
│   └── utils/
│       └── __init__.py
├── static/
│   ├── script/            # Existing scripts
│   ├── scripts/           # New API integration scripts
│   │   ├── supabase-config.js
│   │   ├── student-login-script.js
│   │   ├── faculty-login-script.js
│   │   ├── parent-login-script.js
│   │   └── student-dashboard-script.js
│   └── style/             # CSS files
├── templates/             # HTML templates
├── Dockerfile
├── docker-compose.yml
├── vercel.json
├── requirements.txt
└── .env.example
```

## Database Schema

The application expects the following tables in Supabase:

- `profiles` - User profiles with roles
- `classrooms` - Classroom data with timetable (JSONB)
- `attendance` - Attendance records with periods (JSONB)
- `assignments` - Assignments and tests
- `marks` - Student marks
- `announcements` - Announcements for different roles

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
