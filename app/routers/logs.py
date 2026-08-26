from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/habits", tags=["logs"])
def get_owned_habit(habit_id: int, db: Session, user: models.User) -> models.Habit:
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.user_id == user.id
    ).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.post("/{habit_id}/log", response_model = schemas.HabitLogOut)
def log_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    habit = get_owned_habit(habit_id, db, current_user)
    today = date.today()

    existing = db.query(models.HabitLog).filter(
        models.HabitLog.habit_id == habit.id,
        models.HabitLog.date == today,
    ).first()
    if existing:
        return existing

    new_log = models.HabitLog(habit_id=habit.id, date = today, completed=True)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def calcDaily(complited_dates):
    streak = 0
    day = date.today()
    while day in complited_dates:
        streak+=1
        day -=timedelta(days=1)

    last_7_days = {date.today() - timedelta(days=i) for i in range(7)}
    done_in_week = len(last_7_days & complited_dates)
    completion_rate =done_in_week/7

    return streak,completion_rate

def calcWeekly(complited_dates):
    streak = 0
    day = date.today()
    while day in complited_dates:
        streak+=1
        day -=timedelta(days=1)

    last_7_days = {date.today() - timedelta(days=i) for i in range(7)}
    done_in_week = len(last_7_days & complited_dates)
    completion_rate =done_in_week/7

    return streak,completion_rate

@router.get("/{habit_id}/stats", response_model=schemas.HabitStats)
def habit_stats(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User =Depends(auth.get_current_user),
):
    habit = get_owned_habit(habit_id, db, current_user)
    logs = db.query(models.HabitLog).filter(
        models.HabitLog.habit_id == habit.id,
        models.HabitLog.completed == True
    ).all()
    complited_dates = {log.date for log in logs}

    if habit.frequency == "Weekly":
        streak, completion_rate = calcWeekly(complited_dates)
    else:
        streak, completion_rate = calcDaily(complited_dates)
    

    return schemas.HabitStats(
        habit_id = habit.id,
        current_streak=streak,
        completion_rate_week= round(completion_rate,2)
    )

@router.get("/{habit_id}/history")
def habit_history(
    habit_id: int,
    days: int = 365,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    habit = get_owned_habit(habit_id, db, current_user)
    since = date.today() - timedelta(days=days)

    logs = db.query(models.HabitLog).filter(
        models.HabitLog.habit_id == habit.id,
        models.HabitLog.completed == True,
        models.HabitLog.date >= since,
    ).all()

    return {"dates": [log.date.isoformat() for log in logs]}