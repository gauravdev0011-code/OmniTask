from fastapi import FastAPI
from database import engine
import models

from routes import users, tasks

app = FastAPI(title="OmniTask API")

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": "OmniTask API running"}