from fastapi import FastAPI
from app.routers import auth, companies,applications, dashboard, notes, resumes
import app.models
app=FastAPI()

@app.get("/health")
def welcome():
    return{"message" : "Welcome to Placement tracker"}

app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(applications.router)
app.include_router(notes.router)
app.include_router(dashboard.router)
app.include_router(resumes.router)