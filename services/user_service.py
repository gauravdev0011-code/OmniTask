# services/user_service.py
from sqlalchemy.orm import Session
import models, auth

def register_user(db: Session, username: str, password: str):
    hashed_password = auth.hash_password(password)
    new_user = models.User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()