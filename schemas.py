# schemas.py
from pydantic import BaseModel

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

class TaskUpdate(BaseModel):
    completed: bool