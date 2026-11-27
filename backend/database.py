
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

    # Career assessments table
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

    # Coding assessments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coding_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            skill TEXT NOT NULL,
            topic TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            passed_tests INTEGER,
            total_tests INTEGER,
            score REAL,
            verdict TEXT,
            test_results TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Users table for registration and login
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
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


def get_coding_assessment_history():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM coding_assessments
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    history = []

    for row in rows:
        item = dict(row)
        item["test_results"] = json.loads(item["test_results"])
        history.append(item)

    return history


def save_coding_assessment(data):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO coding_assessments (
            question_id, skill, topic, difficulty,
            passed_tests, total_tests, score,
            verdict, test_results
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["question_id"],
        data["skill"],
        data["topic"],
        data["difficulty"],
        data["passed_tests"],
        data["total_tests"],
        data["score"],
        data["verdict"],
        json.dumps(data["test_results"])
    ))

    connection.commit()
    connection.close()


def get_coding_results_for_mastery():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT skill, topic, difficulty, score
        FROM coding_assessments
        ORDER BY created_at ASC
    """)

    rows = cursor.fetchall()
    connection.close()

    return [dict(row) for row in rows]
