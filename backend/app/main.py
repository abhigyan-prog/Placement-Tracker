from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.core.dependencies import get_db
from app.routers import applications, auth, companies, dashboard, notes, resumes
import app.models

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}


app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(applications.router)
app.include_router(notes.router)
app.include_router(dashboard.router)
app.include_router(resumes.router)
