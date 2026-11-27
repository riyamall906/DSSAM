
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from question_bank.java_questions import JAVA_QUESTIONS
from services.judge0 import submit_code, get_submission_result
from services.scoring import (
    calculate_assessment_score,
    calculate_skill_mastery
)
from services.ai_integration import analyze_with_ai

from database import (
    save_coding_assessment,
    get_coding_assessment_history,
    get_coding_results_for_mastery
)


router = APIRouter(prefix="/assessment", tags=["Assessment"])


# Request models

class CodeSubmission(BaseModel):
    question_id: int
    source_code: str = Field(min_length=1)


class DependencyInput(BaseModel):
    prerequisite: str
    dependent: str
    weight: float = Field(default=1.0, ge=0, le=1)


class AIAnalysisRequest(BaseModel):
    focus_skill: str
    dependencies: List[DependencyInput] = Field(default_factory=list)
    target_mastery: float = Field(default=0.80, ge=0, le=1)
    hours_per_week: float = Field(gt=0)
    comparison_hours_per_week: float = Field(gt=0)
    simulations: int = Field(default=500, ge=1)


# Get coding questions

@router.get("/questions")
def get_questions():
    questions = []

    for question in JAVA_QUESTIONS:
        questions.append({
            "id": question["id"],
            "title": question["title"],
            "skill": question["skill"],
            "topic": question["topic"],
            "difficulty": question["difficulty"],
            "description": question["description"],
            "input": question["input"],
            "output": question["output"],
            "examples": question["examples"]
        })

    return {"questions": questions}


# Submit coding assessment

@router.post("/submit")
def submit_assessment_code(data: CodeSubmission):

    question = next(
        (q for q in JAVA_QUESTIONS if q["id"] == data.question_id),
        None
    )

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    passed = 0
    total = len(question["test_cases"])
    results = []

    for test_case in question["test_cases"]:
        try:
            token = submit_code(
                data.source_code,
                test_case["input"]
            )

            result = get_submission_result(token)
            status = result["status"]["description"]

            if status != "Accepted":
                results.append({
                    "status": status,
                    "passed": False
                })
                continue

            actual = (result.get("stdout") or "").strip()
            expected = test_case["expected_output"].strip()

            is_correct = actual == expected

            if is_correct:
                passed += 1

            results.append({
                "status": "Accepted" if is_correct else "Wrong Answer",
                "passed": is_correct
            })

        except Exception as error:
            raise HTTPException(
                status_code=502,
                detail=f"Judge0 execution failed: {str(error)}"
            )

    score = calculate_assessment_score(results)

    save_coding_assessment({
        "question_id": data.question_id,
        "skill": question["skill"],
        "topic": question["topic"],
        "difficulty": question["difficulty"],
        "passed_tests": passed,
        "total_tests": total,
        "score": score,
        "verdict": "Accepted" if passed == total else "Not Accepted",
        "test_results": results
    })

    return {
        "question_id": data.question_id,
        "passed_tests": passed,
        "total_tests": total,
        "score": score,
        "verdict": "Accepted" if passed == total else "Not Accepted",
        "test_results": results
    }


# Get assessment history

@router.get("/history")
def get_assessment_history():
    return {
        "history": get_coding_assessment_history()
    }


# Calculate skill mastery

@router.get("/mastery")
def get_skill_mastery():

    results = get_coding_results_for_mastery()

    if not results:
        return {"mastery": {}}

    mastery = calculate_skill_mastery(results)

    return {
        "mastery": mastery
    }


# AI Engine integration

@router.post("/analyze")
def analyze_assessment(data: AIAnalysisRequest):

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
