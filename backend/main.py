
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_table

from routes.auth import router as auth_router
from routes.assessment import router as assessment_router
from routes.skills import router as skills_router
from routes.career import router as career_router
from routes.simulation import router as simulation_router

app = FastAPI(title="Distributed Skill Simulation API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(assessment_router)
app.include_router(skills_router)
app.include_router(career_router)
app.include_router(simulation_router)


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
