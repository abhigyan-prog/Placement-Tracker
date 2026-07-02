# Placement Management Platform

A RESTful backend API for managing campus placement processes — built with FastAPI, PostgreSQL, and JWT authentication.

## Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Authentication:** JWT (PyJWT)
- **Validation:** Pydantic

## Project Structure

```
placement-platform/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Settings via pydantic-settings (.env loader)
│   ├── database.py              # DB engine + SessionLocal + Base
│   │
│   ├── models/                  # SQLAlchemy ORM models (DB tables)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── company.py
│   │   ├── application.py
│   │   ├── note.py
│   │   └── resume.py
│   │
│   ├── schemas/                 # Pydantic schemas (request/response shapes)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── company.py
│   │   ├── application.py
│   │   ├── note.py
│   │   └── resume.py
│   │
│   ├── routers/                 # FastAPI route handlers (thin controllers)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── companies.py
│   │   ├── applications.py
│   │   ├── notes.py
│   │   ├── dashboard.py
│   │   └── resumes.py
│   │
│   ├── services/                # Business logic (called by routers)
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── application_service.py
│   │   ├── note_service.py
│   │   └── resume_service.py
│   │
│   └── core/                    # Shared utilities
│       ├── __init__.py
│       ├── security.py          # JWT creation, password hashing
│       └── dependencies.py      # get_db(), get_current_user()
│
├── alembic/                     # Database migrations
│   ├── env.py
│   └── versions/
│
├── .env                         # Secret environment variables (never commit!)
├── .env.example                 # Template for .env (safe to commit)
├── .gitignore
├── requirements.txt
└── README.md
```

## Architecture

The project follows a layered architecture with strict separation of concerns:

```
Request → Router → Service → ORM → PostgreSQL
```

- **Routers** handle HTTP only — parsing requests, returning responses
- **Services** contain all business logic
- **Models** define database structure via SQLAlchemy ORM
- **Schemas** validate incoming data and shape responses via Pydantic

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL

### Installation

```bash
# Clone the repository
git clone https://github.com/abhigyan-prog/Placement-Tracker.git
cd placement-management-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and secret key

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

### Environment Variables

```
DATABASE_URL=postgresql://username:password@localhost:5432/placement_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/auth/me` | Get current authenticated user |
| PATCH | `/auth/me` | Update current user profile |

> CRUD endpoints for companies, applications, notes, and resume upload are under active development.

## API Documentation

Once the server is running, visit:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Roadmap

- [x] Project setup, database connection
- [x] SQLAlchemy ORM models with normalized schema (users, companies, applications, notes, resumes)
- [x] Alembic database migrations
- [x] JWT authentication — register, login, protected routes, update profile
- [ ] Full CRUD for companies and applications with ownership checks
- [ ] Notes CRUD linked to applications
- [ ] Search, filters, and pagination
- [ ] Dashboard stats endpoint
- [ ] Resume PDF upload
- [ ] Tests for auth and core CRUD
