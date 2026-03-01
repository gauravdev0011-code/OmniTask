from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
import schemas
from database import engine, SessionLocal

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="OmniTask API")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------- DATABASE DEPENDENCY ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- USER REGISTER ----------------
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# ---------------- CREATE TASK ----------------
@app.post("/tasks")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):

    new_task = models.Task(
        title=task.title,
        owner_id=task.user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created", "task_id": new_task.id}


# ---------------- GET TASKS ----------------
@app.get("/tasks/{user_id}")
def get_tasks(user_id: int, db: Session = Depends(get_db)):

    tasks = db.query(models.Task).filter(
        models.Task.owner_id == user_id
    ).all()

    return tasks


# ---------------- UPDATE TASK ----------------
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = task_update.completed
    db.commit()

    return {"message": "Task updated"}


# ---------------- DELETE TASK ----------------
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}