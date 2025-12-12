from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    document: str = Field(..., max_length=100)
    phone: Optional[str] = Field(None, max_length=15)
    email: EmailStr
    role: Optional[str] = Field('user', description="user | admin | super")
    horario: Optional[str] = Field(None, description="Mañana|Tarde|Noche")
    department_id: Optional[int]
    position_id: Optional[int]
    qr_path: Optional[str]
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str]
    document: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]
    horario: Optional[str]
    department_id: Optional[int]
    position_id: Optional[int]
    qr_path: Optional[str]
    is_active: Optional[bool]


class UserRead(UserBase):
    id: int
    last_login: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Config:
    orm_mode = True