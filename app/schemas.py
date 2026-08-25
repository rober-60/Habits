from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id:int
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class HabitCreate(BaseModel):
    name: str
    frequency: str

class HabitOut(BaseModel):
    id: int
    name: str
    frequency:str

    class Config:
        from_attributes = True

class HabitLogOut(BaseModel):
    id:int
    date: date
    completed: bool

    class Config:
        from_atributes = True

class HabitStats(BaseModel):
    habit_id: int
    current_streak: int
    completion_rate_week: float

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[str] = None

