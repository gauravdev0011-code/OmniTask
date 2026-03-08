# routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas import UserCreate, UserLogin, UserResponse
from services import user_service

router = APIRouter(tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing = user_service.get_user_by_username(db, user.username)

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    created_user = user_service.register_user(
        db,
        user.username,
        user.password
    )

    return created_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    token = user_service.login_user(
        db,
        user.username,
        user.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }