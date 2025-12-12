# app/schemas.py
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, time, datetime
from app.schemas.user import UserRead

#
# -------------------- ATTENDANCE --------------------
#
class AttendanceBase(BaseModel):
    user_id: int
    date: date
    time_in: Optional[time]
    time_out: Optional[time]
    device_id: Optional[int]
    location: Optional[str]
    status_in: Optional[str] = Field(None, description="Presente|Retardo|Ausente")
    status_out: Optional[str]
    motivo_in: Optional[str]
    motivo_out: Optional[str]
    worked_hours: Optional[float]
    shift_id: Optional[int]

class AttendanceCreate(AttendanceBase):
    # para clocking podrías permitir sólo user_id y timestamp; aquí dejamos campos generales
    pass

class AttendanceUpdate(BaseModel):
    time_in: Optional[time]
    time_out: Optional[time]
    device_id: Optional[int]
    location: Optional[str]
    status_in: Optional[str]
    status_out: Optional[str]
    motivo_in: Optional[str]
    motivo_out: Optional[str]
    worked_hours: Optional[float]
    shift_id: Optional[int]

class AttendanceRead(AttendanceBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # opcional: embed user/shift/device partial info
    user: Optional[UserRead] = None

    class Config:
        orm_mode = True

