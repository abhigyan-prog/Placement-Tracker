# Placement Management Platform

A RESTful backend API for managing campus placement processes — built with FastAPI, PostgreSQL, and JWT authentication.

## Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Authentication:** JWT (PyJWT)
- **Validation:** Pydantic

## Features

- JWT-based user authentication (register, login, protected routes)
- Role-based access for students and admins
- Normalized PostgreSQL schema with version-controlled migrations
- Layered architecture: routers → services → ORM → database
- Interactive API documentation via Swagger UI at `/docs`

## Project Structure

```
placement-management-platform/
├── app/
│   ├── main.py            # FastAPI app entry point
│   ├── database.py        # Database connection and session
│   ├── models/            # SQLAlchemy ORM models
│   ├── schemas/           # Pydantic request/response schemas
│   ├── routers/           # API route handlers
│   ├── services/          # Business logic layer
│   └── auth/              # JWT authentication utilities
├── alembic/               # Database migration files
├── alembic.ini
├── requirements.txt
├── .env.example
└── README.md
```

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

Create a `.env` file in the root directory using `.env.example` as reference:

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

> CRUD endpoints for students, companies, and applications are under active development.

## API Documentation

Once the server is running, visit:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Roadmap

- [x] Project setup and database connection
- [x] SQLAlchemy ORM models with normalized schema
- [x] Alembic database migrations
- [x] JWT authentication — register, login, protected routes
- [ ] CRUD endpoints for students, companies, and applications
- [ ] Search, filters, and pagination
- [ ] Resume PDF upload

