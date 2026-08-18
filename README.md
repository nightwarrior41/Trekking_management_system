# Trekking Management System

A Flask-based web application for managing trekking activities, trekkers, staff, bookings, and administrative operations through role-based access control.

## Overview

The Trekking Management System provides a centralized platform where trekkers can discover and book available treks, staff members can manage the treks assigned to them, and administrators can manage users, staff approvals, treks, and bookings.

The application is built with Flask and uses SQLite with SQLAlchemy for database management. Server-side rendering is implemented using Jinja2 templates, with Bootstrap/CSS for the user interface.

## Features

### 👤 Trekker

- Register and log in securely
- Browse available treks
- Search treks by name
- Filter treks by difficulty and location
- View trek details
- Book a trek
- Prevent duplicate bookings for the same trek
- View personal bookings
- Automatically update available slots after booking

### 🧑‍💼 Trek Staff

- Register as trek staff
- Wait for administrator approval before accessing the system
- View the trek assigned by the administrator
- Update available slots
- Change trek status between Open and Closed

### 🛠️ Administrator

- Access an administrative dashboard
- View system statistics
- Add new treks
- Edit trek information
- Delete treks
- Assign approved staff members to treks
- Approve or reject staff registrations
- Manage trekkers
- Blacklist/unblacklist users
- View and manage all bookings
- Delete bookings and restore the corresponding trek slot
- Search and manage treks and users

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| ORM | Flask-SQLAlchemy / SQLAlchemy |
| Authentication | Flask-Login |
| Forms & Validation | Flask-WTF, WTForms |
| Password Security | Werkzeug password hashing |
| Frontend | HTML, CSS, Bootstrap |
| Templating | Jinja2 |
| Architecture | Flask Application Factory + Blueprints |

## Project Structure

```text
Trekking_app/
│
├── app/
│   ├── forms/
│   │   ├── auth_forms.py
│   │   ├── staff_forms.py
│   │   └── trek_forms.py
│   │
│   ├── routes/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── home.py
│   │   ├── staff.py
│   │   └── user.py
│   │
│   ├── static/
│   │   ├── css/
│   │   └── images/
│   │
│   ├── templates/
│   │   ├── admin/
│   │   ├── auth/
│   │   ├── home/
│   │   ├── staff/
│   │   └── user/
│   │
│   ├── __init__.py
│   ├── auth_loader.py
│   ├── config.py
│   ├── extensions.py
│   └── models.py
│
├── run.py
├── requirement.txt
└── README.md
```

## Database Design

The application uses three primary models:

### User

Stores trekkers, staff members, and administrators.

Important fields include:

- `id`
- `first_name`
- `last_name`
- `email`
- `password`
- `phone`
- `role`
- `is_approved`
- `is_blacklisted`

### Trek

Stores information about each trekking experience.

Important fields include:

- `id`
- `trek_name`
- `location`
- `difficulty`
- `duration`
- `available_slots`
- `status`
- `start_date`
- `end_date`
- `assigned_staff_id`

### Booking

Connects trekkers with the treks they have booked.

Important fields include:

- `id`
- `user_id`
- `trek_id`
- `booking_date`
- `status`

A unique constraint on `user_id` and `trek_id` prevents a user from booking the same trek multiple times.

## Application Flow

```text
                    ┌─────────────────────┐
                    │   Trekking System    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
         ┌─────────┐      ┌──────────┐     ┌─────────┐
         │ Admin   │      │  Staff   │     │ Trekker │
         └────┬────┘      └────┬─────┘     └────┬────┘
              │                │                │
              ▼                ▼                ▼
       Manage Treks      Manage Assigned    Browse Treks
       Manage Users          Trek           Book Treks
       Manage Staff       Update Slots      My Bookings
       Manage Bookings    Update Status
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Trekking_app
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask flask-sqlalchemy flask-login flask-wtf wtforms email-validator
```

### 4. Run the application

```bash
python run.py
```

The application will start on the local Flask development server. Open the address shown in the terminal, typically:

```text
http://127.0.0.1:5000
```

## Database

SQLite is configured in:

```text
app/config.py
```

The database is created automatically using SQLAlchemy when the Flask application starts.

The application does not require manual database-table creation.

## Security

The project includes several security-related mechanisms:

- Passwords are stored using Werkzeug password hashing.
- Flask-Login manages authenticated sessions.
- Role-based access checks protect admin, staff, and trekker routes.
- Staff accounts require administrator approval.
- Blacklisted accounts are prevented from logging in.
- WTForms provides server-side form validation.
- Duplicate trek bookings are prevented using a database-level unique constraint.

> **Development note:** The current project configuration contains a development `SECRET_KEY`. For production deployment, store secrets in environment variables and never commit sensitive credentials to the repository.

## Future Improvements

Some possible extensions for the project include:

- Online payment integration
- Email/SMS booking notifications
- Trek reviews and ratings
- Image uploads for individual treks
- Advanced analytics and reports
- REST API support
- Pagination for large datasets
- Automated booking cancellation
- Deployment using a production WSGI server
- PostgreSQL support for production-scale deployments

## Screenshots

You can add application screenshots here after pushing them to the repository:

```markdown
![Home Page](screenshots/home.png)
![Admin Dashboard](screenshots/admin-dashboard.png)
![Trekker Dashboard](screenshots/user-dashboard.png)
```

## Project Purpose

This project was developed as a full-stack web application to demonstrate practical implementation of:

- Flask application architecture
- Role-based authentication and authorization
- Relational database design
- CRUD operations
- Form validation
- Database relationships
- Booking management
- Server-side rendering
- Modular Flask Blueprints

## License

This project is intended for educational and portfolio purposes.
