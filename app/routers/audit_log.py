# app/routers/audit_logs.py
from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app import deps
from app.crud import audit_log as crud_audit
from app.schemas.audit_log import AuditLogCreate, AuditLogRead

router = APIRouter(prefix="/audit", tags=["audit"])

@router.post("/", response_model=AuditLogRead)
def create_audit(payload: AuditLogCreate, db: Session = Depends(deps.get_db)):
    return crud_audit.create_audit(db, payload)

@router.get("/", response_model=List[AuditLogRead])
def list_audits(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_audit.get_audits(db, skip=skip, limit=limit)
