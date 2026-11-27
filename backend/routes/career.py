
from fastapi import APIRouter, HTTPException
import sqlite3
import json

from database import get_connection

router = APIRouter(prefix="/career", tags=["Career"])


@router.get("/")
def get_careers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT career
        FROM assessments
        ORDER BY career
    """)

    rows = cursor.fetchall()
    connection.close()

    return {
        "careers": [row["career"] for row in rows]
    }


@router.get("/latest")
def get_latest_career_assessment():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM assessments
        ORDER BY created_at DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="No career assessment found"
        )

    result = dict(row)

    json_fields = [
        "skills",
        "weak_skills",
        "intermediate_skills",
        "good_skills",
        "roadmap_details",
        "recommendations"
    ]

    for field in json_fields:
        if result[field]:
            result[field] = json.loads(result[field])

    return {"assessment": result}


@router.get("/{career_name}")
def get_career_assessments(career_name: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM assessments
        WHERE career = ?
        ORDER BY created_at DESC
    """, (career_name,))

    rows = cursor.fetchall()
    connection.close()

    assessments = []

    for row in rows:
        result = dict(row)

        json_fields = [
            "skills",
            "weak_skills",
            "intermediate_skills",
            "good_skills",
            "roadmap_details",
            "recommendations"
        ]

        for field in json_fields:
            if result[field]:
                result[field] = json.loads(result[field])

        assessments.append(result)

    return {
        "career": career_name,
        "assessments": assessments
    }
