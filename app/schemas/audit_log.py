# app/schemas/audit_log.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date, time, datetime

#
# -------------------- AUDIT LOG --------------------
#
class AuditLogBase(BaseModel):
    user_id: Optional[int]
    action: str
    detail: Optional[str]
    ip_address: Optional[str]

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogRead(AuditLogBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


