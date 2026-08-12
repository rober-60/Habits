from fastapi import FastAPI
from app.routers import auth,habits

app = FastAPI(title="Habit Tracker API")

app.include_router(auth.router)
app.include_router(habits.router)


@app.get("/")
def root():
    return {"status": "ok"}