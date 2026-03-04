# services/task_service.py
from sqlalchemy.orm import Session
import models

# CREATE TASK
def create_task(db: Session, title: str, user_id: int):
    new_task = models.Task(title=title, owner_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# GET TASKS FOR USER
def get_tasks_by_user(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

# UPDATE TASK
def update_task(db: Session, task_id: int, completed: bool):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None
    task.completed = completed
    db.commit()
    db.refresh(task)
    return task

# DELETE TASK
def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True