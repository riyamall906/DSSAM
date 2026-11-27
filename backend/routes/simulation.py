
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from database import get_coding_results_for_mastery
from services.ai_integration import analyze_with_ai

router = APIRouter(prefix="/simulation", tags=["Simulation"])


class DependencyInput(BaseModel):
    prerequisite: str
    dependent: str
    weight: float = Field(default=1.0, ge=0, le=1)


class SimulationRequest(BaseModel):
    focus_skill: str
    dependencies: List[DependencyInput] = Field(default_factory=list)
    target_mastery: float = Field(default=0.80, ge=0, le=1)
    hours_per_week: float = Field(gt=0)
    comparison_hours_per_week: float = Field(gt=0)
    simulations: int = Field(default=500, ge=1)


@router.post("/run")
def run_simulation(data: SimulationRequest):

    results = get_coding_results_for_mastery()

    if not results:
        raise HTTPException(
            status_code=400,
            detail="No coding assessment results found"
        )

    skills = list(dict.fromkeys(
        result["skill"] for result in results
    ))

    if data.focus_skill not in skills:
        raise HTTPException(
            status_code=400,
            detail="Focus skill not found in assessment results"
        )

    submissions = [
        {
            "skill": result["skill"],
            "correct": result["score"] == 100
        }
        for result in results
    ]

    payload = {
        "skills": skills,
        "submissions": submissions,
        "dependencies": [
            dependency.model_dump()
            for dependency in data.dependencies
        ],
        "focus_skill": data.focus_skill,
        "target_mastery": data.target_mastery,
        "hours_per_week": data.hours_per_week,
        "comparison_hours_per_week": data.comparison_hours_per_week,
        "simulations": data.simulations
    }

    try:
        return analyze_with_ai(payload)

    except RuntimeError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )
