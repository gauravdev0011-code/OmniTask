# routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

import models
import schemas
from database import SessionLocal

router = APIRouter(tags=["Tasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE TASK
@router.post("/tasks")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):

    new_task = models.Task(
        title=task.title,
        owner_id=task.user_id,
        priority=task.priority,
        due_date=task.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# GET USER TASKS
@router.get("/tasks/{user_id}")
def get_tasks(user_id: int, db: Session = Depends(get_db)):

    tasks = db.query(models.Task).filter(
        models.Task.owner_id == user_id
    ).all()

    return tasks


# UPDATE TASK
@router.put("/tasks/{task_id}")
def update_task(task_id: int, update: schemas.TaskUpdate,
                db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if update.completed is not None:
        task.completed = update.completed

    if update.status is not None:
        task.status = update.status

    if update.priority is not None:
        task.priority = update.priority

    if update.due_date is not None:
        task.due_date = update.due_date

    db.commit()
    db.refresh(task)

    return task


# DELETE TASK
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}


# OVERDUE TASKS
@router.get("/tasks/overdue")
def get_overdue_tasks(db: Session = Depends(get_db)):

    tasks = db.query(models.Task).filter(
        models.Task.due_date < datetime.utcnow(),
        models.Task.completed == False
    ).all()

    return tasks