# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date, time, datetime

#
# -------------------- DEVICE --------------------
#
class DeviceBase(BaseModel):
    identifier: str
    location: Optional[str]

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    identifier: Optional[str]
    location: Optional[str]

class DeviceRead(DeviceBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
