# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date, time, datetime

#
# -------------------- DEPARTMENT --------------------
#
class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    manager_id: Optional[int]

class DepartmentUpdate(BaseModel):
    name: Optional[str]
    manager_id: Optional[int]

class DepartmentRead(DepartmentBase):
    id: int
    manager_id: Optional[int]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

