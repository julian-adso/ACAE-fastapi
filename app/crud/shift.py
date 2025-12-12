# app/crud/shifts.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.shift import Shift
from app.schemas.shift import ShiftCreate, ShiftUpdate

def get_shift(db: Session, id: int) -> Optional[Shift]:
    return db.query(Shift).filter(Shift.id == id).first()

def get_shifts(db: Session, skip: int = 0, limit: int = 100) -> List[Shift]:
    return db.query(Shift).offset(skip).limit(limit).all()

def create_shift(db: Session, payload: ShiftCreate) -> Shift:
    s = Shift(name=payload.name, start_time=payload.start_time, end_time=payload.end_time, grace_period=payload.grace_period or 10)
    db.add(s); db.commit(); db.refresh(s)
    return s

def update_shift(db: Session, shift: Shift, payload: ShiftUpdate) -> Shift:
    data = payload.dict(exclude_unset=True)
    for k,v in data.items():
        setattr(shift, k, v)
    db.add(shift); db.commit(); db.refresh(shift)
    return shift

def delete_shift(db: Session, shift: Shift):
    db.delete(shift); db.commit()
