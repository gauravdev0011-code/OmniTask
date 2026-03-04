# routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import TaskCreate, TaskUpdate
from services import task_service

router = APIRouter(tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    created = task_service.create_task(db, task.title, task.user_id)
    return {"message": "Task created", "task_id": created.id}

@router.get("/tasks/{user_id}")
def get_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = task_service.get_tasks_by_user(db, user_id)
    return tasks

@router.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate, db: Session = Depends(get_db)):
    updated = task_service.update_task(db, task_id, update.completed)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated"}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = task_service.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}