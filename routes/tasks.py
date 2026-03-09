# routes/tasks.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

import models
import schemas
from dependencies import get_db, get_current_user
from logger import logger

router = APIRouter(tags=["Tasks"])


@router.post("/tasks", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    new_task = models.Task(
        title=task.title,
        owner_id=current_user.id,
        priority=task.priority,
        due_date=task.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info(f"Task created by user {current_user.username}")

    return new_task


@router.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    query = db.query(models.Task).filter(
        models.Task.owner_id == current_user.id
    )

    if status:
        query = query.filter(models.Task.status == status)

    if priority:
        query = query.filter(models.Task.priority == priority)

    if completed is not None:
        query = query.filter(models.Task.completed == completed)

    tasks = query.offset(skip).limit(limit).all()

    return tasks


@router.get("/tasks/search", response_model=List[schemas.TaskResponse])
def search_tasks(
    q: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    tasks = db.query(models.Task).filter(
        models.Task.owner_id == current_user.id,
        models.Task.title.ilike(f"%{q}%")
    ).all()

    return tasks


@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
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

    logger.info(f"Task {task_id} updated by {current_user.username}")

    return task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    logger.info(f"Task {task_id} deleted by {current_user.username}")

    return {"message": "Task deleted"}