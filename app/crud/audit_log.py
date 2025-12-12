# app/crud/audit_logs.py
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate

def create_audit(db: Session, payload: AuditLogCreate) -> AuditLog:
    a = AuditLog(user_id=payload.user_id, action=payload.action, detail=payload.detail, ip_address=payload.ip_address)
    db.add(a); db.commit(); db.refresh(a)
    return a

def get_audits(db: Session, skip: int=0, limit: int=100) -> List[AuditLog]:
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
