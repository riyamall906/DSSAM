
import sqlite3
import json

DATABASE_NAME = "dssam.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            career TEXT NOT NULL,
            overall_score INTEGER,
            skills TEXT,
            weak_skills TEXT,
            intermediate_skills TEXT,
            good_skills TEXT,
            roadmap_details TEXT,
            recommendations TEXT,
            total_learning_hours REAL,
            estimated_days INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_assessment(data):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO assessments (
            career, overall_score, skills,
            weak_skills, intermediate_skills,
            good_skills, roadmap_details,
            recommendations, total_learning_hours,
            estimated_days
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["career"],
        data["overall_score"],
        json.dumps(data["skills"]),
        json.dumps(data["weak_skills"]),
        json.dumps(data["intermediate_skills"]),
        json.dumps(data["good_skills"]),
        json.dumps(data["roadmap_details"]),
        json.dumps(data["recommendations"]),
        data["total_learning_hours"],
        data["estimated_days"]
    ))

    connection.commit()
    connection.close()

def get_assessment_history():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM assessments
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    history = []

    for row in rows:
        item = dict(row)

        item["skills"] = json.loads(item["skills"])
        item["weak_skills"] = json.loads(item["weak_skills"])
        item["intermediate_skills"] = json.loads(item["intermediate_skills"])
        item["good_skills"] = json.loads(item["good_skills"])
        item["roadmap_details"] = json.loads(item["roadmap_details"])
        item["recommendations"] = json.loads(item["recommendations"])

        history.append(item)

    return history
