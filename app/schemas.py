# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------------- USER ----------------

class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# ---------------- TASK ----------------

class TaskCreate(BaseModel):
    title: str
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    completed: Optional[bool] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    status: str
    priority: str
    due_date: Optional[datetime]
    owner_id: int

    class Config:
        from_attributes = True