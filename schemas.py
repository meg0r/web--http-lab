from pydantic import BaseModel, Field
from typing import Optional

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=80)
    content: str = Field(..., min_length=1, max_length=500)

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=80)
    content: Optional[str] = Field(None, min_length=1, max_length=500)

class UserCreate(BaseModel):
    email: str=Field(...,min_length=1,description="Электронная почта пользователя")
    password: str = Field(...,min_length=6,description="Пароль (минимум 6 символов")

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str