# app/schemas/password_reset_token.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date, time, datetime

#
# -------------------- PASSWORD RESET TOKEN --------------------
#
class PasswordResetTokenBase(BaseModel):
    user_id: int
    token: str
    expires_at: datetime

class PasswordResetTokenCreate(PasswordResetTokenBase):
    pass

class PasswordResetTokenRead(PasswordResetTokenBase):
    id: int
    used: Optional[bool] = False
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
