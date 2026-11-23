
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

from .skill_analyzer import SkillAnalyzer
from .skill_graph import SkillGraph
from .skill_debt import SkillDebtAnalyzer
from .route_simulator import RouteSimulator
from .learning_routes import LearningRouteGenerator
from .what_if import WhatIfAnalyzer


app = FastAPI(
    title="DSSAM AI Engine API",
    description="Skill analysis and learning route generation",
    version="1.0"
)


class Submission(BaseModel):
    skill: str
    correct: bool


class Dependency(BaseModel):
    prerequisite: str
    dependent: str
    weight: float = Field(default=1.0, ge=0, le=1)


class AnalysisRequest(BaseModel):
    skills: List[str]
    submissions: List[Submission]
    dependencies: List[Dependency]

    focus_skill: str
    target_mastery: float = Field(default=0.80, ge=0, le=1)

    hours_per_week: float = Field(gt=0)
    comparison_hours_per_week: float = Field(gt=0)

    simulations: int = Field(default=500, ge=1)


@app.get("/")
def home():
    return {
        "message": "DSSAM AI Engine API is running"
    }


@app.post("/analyze")
def analyze_skills(request: AnalysisRequest):

    try:
        if not request.skills:
            raise HTTPException(
                status_code=400,
                detail="At least one skill is required"
            )

        if len(set(request.skills)) != len(request.skills):
            raise HTTPException(
                status_code=400,
                detail="Duplicate skills are not allowed"
            )

        if request.focus_skill not in request.skills:
            raise HTTPException(
                status_code=400,
                detail="Focus skill must exist in the skills list"
            )

        analyzer = SkillAnalyzer()

        for skill in request.skills:
            analyzer.add_skill(skill)

        for submission in request.submissions:

            if submission.skill not in request.skills:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unknown skill: {submission.skill}"
                )

            analyzer.update_mastery(
                submission.skill,
                submission.correct
            )

        mastery = {
            skill: value / 100
            for skill, value in analyzer.get_all_mastery().items()
        }

        uncertainty = {
            skill: value / 100
            for skill, value in analyzer.get_all_uncertainty().items()
        }

        skill_graph = SkillGraph()

        for skill in request.skills:
            skill_graph.add_skill(skill)

        for dependency in request.dependencies:

            if (
                dependency.prerequisite not in request.skills
                or dependency.dependent not in request.skills
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Dependency contains an unknown skill"
                )

            skill_graph.add_dependency(
                dependency.prerequisite,
                dependency.dependent,
                dependency.weight
            )

        debt_analyzer = SkillDebtAnalyzer(skill_graph.graph)
        debt = debt_analyzer.calculate_debt(mastery)

        simulator = RouteSimulator(
            simulations=request.simulations
        )

        focus = request.focus_skill

        simulation_result = simulator.estimate_learning_time(
            current_mastery=mastery[focus],
            target_mastery=request.target_mastery,
            hours_per_week=request.hours_per_week,
            skill_debt=debt[focus],
            uncertainty=uncertainty[focus]
        )

        route_generator = LearningRouteGenerator(
            mastery,
            debt,
            skill_graph.graph
        )

        routes = route_generator.generate_routes()

        what_if_analyzer = WhatIfAnalyzer(simulator)

        what_if_result = what_if_analyzer.compare_learning_plans(
            current_mastery=mastery[focus],
            target_mastery=request.target_mastery,
            skill_debt=debt[focus],
            uncertainty=uncertainty[focus],
            current_hours=request.hours_per_week,
            new_hours=request.comparison_hours_per_week
        )

        return {
            "skill_mastery": {
                skill: round(value * 100, 2)
                for skill, value in mastery.items()
            },
            "mastery_uncertainty": {
                skill: round(value * 100, 2)
                for skill, value in uncertainty.items()
            },
            "skill_debt": debt,
            "focus_skill": focus,
            "learning_time": simulation_result,
            "learning_routes": routes,
            "what_if_analysis": what_if_result
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
