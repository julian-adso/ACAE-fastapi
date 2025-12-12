# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date, time, datetime

#
# -------------------- HOLIDAY --------------------
#
class HolidayBase(BaseModel):
    date: date
    name: Optional[str]

class HolidayCreate(HolidayBase):
    pass

class HolidayUpdate(BaseModel):
    date: Optional[date]
    name: Optional[str]

class HolidayRead(HolidayBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

