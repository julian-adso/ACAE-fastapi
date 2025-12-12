# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date, time, datetime

#
# -------------------- SHIFT --------------------
#
class ShiftBase(BaseModel):
    name: str
    start_time: time
    end_time: time
    grace_period: Optional[int] = 10  # minutos

class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(BaseModel):
    name: Optional[str]
    start_time: Optional[time]
    end_time: Optional[time]
    grace_period: Optional[int]

class ShiftRead(ShiftBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
