# routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import UserCreate, UserLogin
from services import user_service

router = APIRouter(tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- REGISTER ----
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = user_service.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    created_user = user_service.register_user(db, user.username, user.password)
    return {"message": "User registered", "user_id": created_user.id}

# ---- LOGIN ----
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = user_service.login_user(db, user.username, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": token, "token_type": "bearer"}