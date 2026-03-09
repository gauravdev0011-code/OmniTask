# services/user_service.py

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt

import models
import auth
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def register_user(db: Session, username: str, password: str):
    hashed_password = auth.hash_password(password)

    new_user = models.User(
        username=username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username
    ).first()


def login_user(db: Session, username: str, password: str):

    user = get_user_by_username(db, username)

    if not user:
        return None

    if not auth.verify_password(password, user.password):
        return None

    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return token


def create_access_token(data: dict, expires_delta: timedelta | None = None):

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt