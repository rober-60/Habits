from fastapi import FastAPI

app = FastAPI(title="Habit Tracker API")


@app.get("/")
def root():
    return {"status": "ok"}