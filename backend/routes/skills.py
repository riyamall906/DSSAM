
from fastapi import APIRouter

from database import get_coding_results_for_mastery
from services.scoring import calculate_skill_mastery

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("/")
def get_skills():
    results = get_coding_results_for_mastery()

    skills = sorted(set(
        result["skill"] for result in results
    ))

    return {"skills": skills}


@router.get("/mastery")
def get_skills_mastery():
    results = get_coding_results_for_mastery()

    if not results:
        return {"mastery": {}}

    mastery = calculate_skill_mastery(results)

    return {"mastery": mastery}


@router.get("/details")
def get_skill_details():
    results = get_coding_results_for_mastery()

    details = {}

    for result in results:
        skill = result["skill"]

        if skill not in details:
            details[skill] = {
                "topics": [],
                "difficulties": []
            }

        if result["topic"] not in details[skill]["topics"]:
            details[skill]["topics"].append(result["topic"])

        if result["difficulty"] not in details[skill]["difficulties"]:
            details[skill]["difficulties"].append(result["difficulty"])

    return {"details": details}
