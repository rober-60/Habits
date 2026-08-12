from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
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
    frequency: str

    class Config:
        from_attributes = True
