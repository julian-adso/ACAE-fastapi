# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date, time, datetime

#
# -------------------- ATTENDANCE CORRECTION --------------------
#
class AttendanceCorrectionBase(BaseModel):
    attendance_id: int
    requester_id: int
    reason: str

class AttendanceCorrectionCreate(AttendanceCorrectionBase):
    pass

class AttendanceCorrectionUpdate(BaseModel):
    status: Optional[str]  # pending | approved | rejected
    reviewed_by: Optional[int]

class AttendanceCorrectionRead(AttendanceCorrectionBase):
    id: int
    requested_at: Optional[datetime]
    status: Optional[str]
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]

    class Config:
        orm_mode = True

