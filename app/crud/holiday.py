# app/crud/holidays.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.holiday import Holiday
from app.schemas.holiday import HolidayCreate, HolidayUpdate

def get_holiday(db: Session, id: int) -> Optional[Holiday]:
    return db.query(Holiday).filter(Holiday.id == id).first()

def get_holidays(db: Session, skip: int = 0, limit: int = 100) -> List[Holiday]:
    return db.query(Holiday).order_by(Holiday.date).offset(skip).limit(limit).all()

def create_holiday(db: Session, payload: HolidayCreate) -> Holiday:
    h = Holiday(date=payload.date, name=payload.name)
    db.add(h); db.commit(); db.refresh(h)
    return h

def update_holiday(db: Session, holiday: Holiday, payload: HolidayUpdate) -> Holiday:
    data = payload.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(holiday, k, v)
    db.add(holiday); db.commit(); db.refresh(holiday)
    return holiday

def delete_holiday(db: Session, holiday: Holiday):
    db.delete(holiday); db.commit()
