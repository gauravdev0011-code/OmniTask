from pydantic import BaseModel
from datetime import datetime


# -------- USER --------

class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# -------- TASK --------

class TaskCreate(BaseModel):
    title: str
    user_id: int
    priority: str | None = "medium"
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    completed: bool | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None