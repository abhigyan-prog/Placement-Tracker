from fastapi import FastAPI
from app.routers import auth, companies
import app.models
app=FastAPI()

@app.get("/")
def welcome():
    return{"message" : "Welcome to Placement tracker"}

app.include_router(auth.router)
app.include_router(companies.router)