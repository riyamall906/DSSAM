from fastapi import FastAPI
from database import create_table
from routes.assessment import router as assessment_router

app = FastAPI(title="Distributed Skill Simulation API")
app.include_router(assessment_router)

@app.on_event("startup")
def startup():
    create_table()


@app.get("/")
def home():
    return {
        "message": "Distributed Skill Simulation Backend is Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }