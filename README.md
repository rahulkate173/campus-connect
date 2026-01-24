# Campus Connect - College Management System

A comprehensive college management system with three portals: Student, Parent, and Teacher. Built with Flask/FastAPI backend and Supabase database, deployable on Vercel.

Contributors

- Rahul Kate
- Aditya Tilekar
- Siddesh Tarle
- Padmaraj Pawar


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
