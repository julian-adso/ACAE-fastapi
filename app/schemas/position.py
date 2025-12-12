# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date, time, datetime

#
# -------------------- POSITION --------------------
#
class PositionBase(BaseModel):
    name: str

class PositionCreate(PositionBase):
    pass

class PositionUpdate(BaseModel):
    name: Optional[str]

class PositionRead(PositionBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
