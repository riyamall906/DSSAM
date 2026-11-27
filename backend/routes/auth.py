
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import sqlite3

from database import get_connection
from services.auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

security = HTTPBearer(auto_error=False)


# Request models

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: str
    password: str


# Registration API

@router.post("/register")
def register_user(data: RegisterRequest):

    name = data.name.strip()
    email = data.email.strip().lower()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )

    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(
            status_code=400,
            detail="Invalid email address"
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
        """, (
            name,
            email,
            hash_password(data.password)
        ))

        user_id = cursor.lastrowid
        connection.commit()

        return {
            "message": "Registration successful",
            "user": {
                "id": user_id,
                "name": name,
                "email": email
            }
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    finally:
        connection.close()


# Login API

@router.post("/login")
def login_user(data: LoginRequest):

    email = data.email.strip().lower()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, password_hash
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    connection.close()

    if user is None or not verify_password(
        data.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(user["id"])

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }


# Get logged-in user

@router.get("/me")
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication token required"
        )

    user_id = verify_access_token(credentials.credentials)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()
    connection.close()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"user": dict(user)}
