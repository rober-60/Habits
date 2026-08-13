from fastapi import FastAPI
from app.routers import auth,habits,logs

app = FastAPI(title="Habit Tracker API")

app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(logs.router)

@app.get("/")
def root():
    return {"status": "ok"}