from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/habits", tags=["habits"])

@router.post("/", response_model=schemas.HabitOut)
def create_habit(
    habit: schemas.HabitCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    new_habit = models.Habit(
        name=habit.name,
        frequency=habit.frequency,
        user_id=current_user.id,
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit

@router.get("/", response_model=list[schemas.HabitOut])
def list_habits(db: Session = Depends(get_db),current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Habit).filter(models.Habit.user_id == current_user.id).all()

@router.delete("/{habit_id}")
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.user_id == current_user.id,
    ).first()

    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    db.delete(habit)
    db.commit()
    return {"detail": "Habit deleted"}