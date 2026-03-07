# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# USER SCHEMAS

class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# TASK SCHEMAS

class TaskCreate(BaseModel):
    title: str
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    completed: Optional[bool] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None