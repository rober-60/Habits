from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="Habit Tracker API")

app.include_router(auth.router)


@app.get("/")
def root():
    return {"status": "ok"}