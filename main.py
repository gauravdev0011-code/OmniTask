from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from passlib.context import CryptContext

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# USER REGISTER
@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    new_user = models.User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


# CREATE TASK
@app.post("/tasks")
def create_task(title: str, user_id: int, db: Session = Depends(get_db)):
    task = models.Task(title=title, owner_id=user_id)
    db.add(task)
    db.commit()
    return {"message": "Task created"}


# GET TASKS
@app.get("/tasks/{user_id}")
def get_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == user_id).all()
    return tasks


# UPDATE TASK
@app.put("/tasks/{task_id}")
def update_task(task_id: int, completed: bool, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = completed
    db.commit()
    return {"message": "Task updated"}


# DELETE TASK
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}