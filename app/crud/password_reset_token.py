# app/crud/password_reset_tokens.py
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
import secrets
from app.models.password_reset_token import PasswordResetToken

def create_reset_token(db: Session, user_id: int, expiry_minutes: int = 60) -> PasswordResetToken:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    pr = PasswordResetToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(pr); db.commit(); db.refresh(pr)
    return pr

def get_reset_token(db: Session, token: str) -> Optional[PasswordResetToken]:
    return db.query(PasswordResetToken).filter(PasswordResetToken.token == token, PasswordResetToken.used == False).first()

def mark_token_used(db: Session, token_obj: PasswordResetToken):
    token_obj.used = True
    db.add(token_obj); db.commit()
