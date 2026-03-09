# main.py

from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

import models
from database import engine
from routes import users, tasks

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="OmniTask API")

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": "OmniTask API running"}