# Placement Tracker

A full-stack application for organizing the job search. Track applications from
submission through offer, keep company and interview notes together, and manage
the resume versions used for applications.

**Live Website:** https://placement-tracker-abhigyan8.vercel.app/

## What it does

- **Application tracking:** Create and update applications, change their status,
  and search or filter by company, role, status, and date.
- **Company records:** Keep company details in one place and associate them
  with applications.
- **Notes:** Save general notes or notes associated with a company or
  application.
- **Resume management:** Upload PDF resume versions, choose an active version,
  and associate resumes with applications.
- **Dashboard:** Review application totals and status summaries.
- **Accounts:** Register and sign in with JWT authentication. API resources are
  scoped to the signed-in user.

## Project highlights

- FastAPI routers delegate application logic to service modules.
- Pydantic schemas validate request data and define API responses.
- SQLAlchemy models and Alembic migrations manage the PostgreSQL schema.
- The React client uses a shared API helper and feature-based views.
- The health endpoint checks database connectivity as well as API availability.

## Technology

| Area | Technologies |
| --- | --- |
| Frontend | React, Vite, JavaScript |
| API | Python, FastAPI, Pydantic |
| Database | PostgreSQL, SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT |
| Resume storage | Supabase Storage |

## Repository structure

```text
backend/
  app/
    core/         Authentication and shared dependencies
    models/       SQLAlchemy models
    routers/      API endpoints
    schemas/      Request and response schemas
    services/     Application logic
  alembic/        Database migrations
  tests/          Backend tests
frontend/
  src/
    api/          API client
    components/   Shared UI
    features/     Dashboard and tracker screens
```

## Getting started

### Requirements

- Python 3.10+
- PostgreSQL
- Node.js 20.19+ or 22.12+
- A Supabase project with a storage bucket for resumes

### Configure and run the API

From the repository root:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set the values in `backend/.env`, then apply the migrations and start the API:

```powershell
alembic upgrade head
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`. Interactive documentation is
at `http://localhost:8000/docs`.

### Run the frontend

In a second terminal, from the repository root:

```powershell
cd frontend
npm ci
npm run dev
```

For local development, the frontend defaults to the API at
`http://localhost:8000`. Set `VITE_API_URL` if the API uses a different origin.
For production builds, set `VITE_API_URL` to the deployed API URL.

## Configuration

The backend reads the following values from its environment or `backend/.env`:

| Variable | Description |
| --- | --- |
| `SQLALCHEMY_DATABASE_URL` | PostgreSQL connection URL |
| `SECRET_KEY` | Secret used to sign JWT access tokens |
| `ALGORITHM` | JWT signing algorithm, typically `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access-token lifetime |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SECRET_KEY` | Server-side Supabase key used by the API |
| `SUPABASE_BUCKET` | Storage bucket for resume PDFs (defaults to `resumes`) |

Never commit `.env` files or production secrets.

## API overview

Protected routes require an `Authorization: Bearer <token>` header. Login
accepts a JSON body containing `email` and `password`.

| Feature | Endpoints |
| --- | --- |
| Authentication | `POST /auth/register`, `POST /auth/login`, `GET /auth/me`, `PATCH /auth/me` |
| Companies | `GET` and `POST /companies/`; `GET`, `PATCH`, and `DELETE /companies/{id}` |
| Applications | `GET` and `POST /applications/`; `GET`, `PATCH`, and `DELETE /applications/{id}` |
| Application status | `PATCH /applications/{id}/status` |
| Application notes | `GET /applications/{id}/notes` |
| Notes | `GET` and `POST /notes/`; `GET`, `PATCH`, and `DELETE /notes/{id}` |
| Dashboard | `GET /dashboard/` |
| Resumes | `GET` and `POST /resumes/`; `GET`, `PATCH`, and `DELETE /resumes/{id}` |
| Activate a resume | `PATCH /resumes/{id}/activate` |
| Health check | `GET /health` |

Application listing supports status, company, role, and date filters, along
with `page` and `limit` pagination parameters.

## Deployment

The API can be deployed as a Render web service with `backend` as its root
directory. Use the following build commands:

```bash
pip install -r requirements.txt
alembic upgrade head
```

Use this start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Configure the backend environment variables listed above, including
`CORS_ORIGINS` for the deployed frontend's origin.

For Vercel, set `frontend` as the root directory, use `npm run build` as the
build command, and `dist` as the output directory. Set `VITE_API_URL` to the
deployed API URL in the Vercel project environment before building.

The API uses Neon for PostgreSQL and Supabase Storage for resume files. Set the
Supabase URL, server-side key, and bucket name in the Render backend environment.
Do not expose the Supabase secret key through frontend environment variables.
