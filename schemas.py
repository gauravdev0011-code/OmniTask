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
    priority: str = "medium"
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    completed: bool
    status: str
    priority: str
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    status: str
    priority: str
    due_date: datetime | None
    owner_id: int

    class Config:
        orm_mode = True