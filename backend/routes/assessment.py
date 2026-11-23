
from fastapi import APIRouter
from question_bank.java_questions import JAVA_QUESTIONS

router = APIRouter(prefix="/assessment", tags=["Assessment"])


@router.get("/questions")
def get_questions():
    questions = []

from pydantic import BaseModel, Field
from services.judge0 import submit_code, get_submission_result


class CodeSubmission(BaseModel):
    question_id: int
    source_code: str = Field(min_length=1)


@router.post("/submit")
def submit_assessment_code(data: CodeSubmission):
    question = next(
        (q for q in JAVA_QUESTIONS if q["id"] == data.question_id),
        None
    )

    if question is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Question not found")

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
            from fastapi import HTTPException
            raise HTTPException(
                status_code=502,
                detail=f"Judge0 execution failed: {str(error)}"
            )

    return {
        "question_id": data.question_id,
        "passed_tests": passed,
        "total_tests": total,
        "verdict": "Accepted" if passed == total else "Not Accepted",
        "test_results": results
    }



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
