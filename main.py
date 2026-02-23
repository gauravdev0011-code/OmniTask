from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "OmniTask backend is running"}