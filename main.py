# main.py
from fastapi import FastAPI
from database import engine
import models
from routes import users, tasks

app = FastAPI(title="OmniTask API")

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "OmniTask API running"}