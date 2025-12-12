# app/crud/corrections.py
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.attendance_correction import AttendanceCorrection
from app.schemas.attendance_correction import AttendanceCorrectionCreate, AttendanceCorrectionUpdate
from app.models.attendance import Attendance

def get_correction(db: Session, id: int) -> Optional[AttendanceCorrection]:
    return db.query(AttendanceCorrection).filter(AttendanceCorrection.id == id).first()

def get_corrections(db: Session, skip: int = 0, limit: int = 100) -> List[AttendanceCorrection]:
    return db.query(AttendanceCorrection).offset(skip).limit(limit).all()

def request_correction(db: Session, payload: AttendanceCorrectionCreate) -> AttendanceCorrection:
    c = AttendanceCorrection(attendance_id=payload.attendance_id, requester_id=payload.requester_id, reason=payload.reason)
    db.add(c); db.commit(); db.refresh(c)
    return c

def review_correction(db: Session, correction: AttendanceCorrection, reviewer_id: int, approve: bool, new_values: dict = None) -> AttendanceCorrection:
    correction.status = "approved" if approve else "rejected"
    correction.reviewed_by = reviewer_id
    correction.reviewed_at = datetime.utcnow()
    db.add(correction)

    if approve and new_values:
        # apply changes to attendance
        att = db.query(Attendance).filter(Attendance.id == correction.attendance_id).first()
        if att:
            for k, v in new_values.items():
                setattr(att, k, v)
            db.add(att)

    db.commit()
    db.refresh(correction)
    return correction
