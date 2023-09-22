from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class User(BaseModel):
    name: str
    email: EmailStr
    password: str

class ShowUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    class Config():
        from_attributes = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

class Movie(BaseModel):
    id: int
    film_id: int
    title: str
    genre: str
    overview: str
    image: str

class Score(BaseModel):
    user_id: int
    film_id: int
    value: float = Field(..., ge=0, le=5)

class ShowScore(BaseModel):
    id: int
    user_id: int
    film_id: int
    value: float = Field(..., ge=0, le=5)

    class Config():
        from_attributes = True

class ConfirmationEmail(BaseModel):
    email: str
    confirmation_link: str
