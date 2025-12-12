# app/crud/attendance.py
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, date, time, timedelta
from app.models.attendance import Attendance
from app.models.shift import Shift
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate

def get_attendance(db: Session, id: int) -> Optional[Attendance]:
    return db.query(Attendance).filter(Attendance.id == id).first()

def get_attendances(db: Session, skip: int = 0, limit: int = 100) -> List[Attendance]:
    return db.query(Attendance).offset(skip).limit(limit).all()

def get_attendances_for_user(db: Session, user_id: int, from_date: date=None, to_date: date=None):
    q = db.query(Attendance).filter(Attendance.user_id == user_id)
    if from_date:
        q = q.filter(Attendance.date >= from_date)
    if to_date:
        q = q.filter(Attendance.date <= to_date)
    return q.order_by(Attendance.date).all()

def create_attendance(db: Session, payload: AttendanceCreate) -> Attendance:
    a = Attendance(**payload.dict(exclude_unset=True))
    db.add(a); db.commit(); db.refresh(a)
    return a

def update_attendance(db: Session, att: Attendance, payload: AttendanceUpdate) -> Attendance:
    data = payload.dict(exclude_unset=True)
    for k,v in data.items():
        setattr(att, k, v)
    # recalc worked_hours if times present
    if att.time_in and att.time_out:
        dt_in = datetime.combine(att.date, att.time_in)
        dt_out = datetime.combine(att.date, att.time_out)
        delta = dt_out - dt_in
        att.worked_hours = delta.total_seconds() / 3600.0
    db.add(att); db.commit(); db.refresh(att)
    return att

def delete_attendance(db: Session, att: Attendance):
    db.delete(att); db.commit()

#
# Clock in/out helper
#
def clock_in_out(db: Session, user_id: int, timestamp: Optional[datetime]=None, device_id: Optional[int]=None, location: Optional[str]=None) -> Attendance:
    """
    Logic:
      - determine today's attendance row by date
      - if row doesn't exist: create with time_in = timestamp.time()
      - elif exists and time_out is null: set time_out = timestamp.time()
      - else: create new row (multiple punches)
      - compute worked_hours
      - compute status_in comparing with shift (if shift assigned)
    """
    ts = timestamp or datetime.utcnow()
    day = ts.date()
    att = db.query(Attendance).filter(Attendance.user_id == user_id, Attendance.date == day).first()

    if att is None:
        att = Attendance(user_id=user_id, date=day, time_in=ts.time(), device_id=device_id, location=location)
        db.add(att)
        db.commit()
        db.refresh(att)
    else:
        if att.time_in is None:
            att.time_in = ts.time()
        elif att.time_out is None:
            att.time_out = ts.time()
        else:
            # already has in and out: create new attendance row (multiple shifts)
            att = Attendance(user_id=user_id, date=day, time_in=ts.time(), device_id=device_id, location=location)
            db.add(att)
            db.commit()
            db.refresh(att)

    # compute worked_hours and status_in if possible
    if att.time_in and att.time_out:
        from datetime import datetime as dt
        dt_in = dt.combine(att.date, att.time_in)
        dt_out = dt.combine(att.date, att.time_out)
        att.worked_hours = (dt_out - dt_in).total_seconds()/3600.0

    # attempt to compute status using assigned shift
    if att.shift_id:
        shift = db.query(Shift).filter(Shift.id == att.shift_id).first()
        if shift and att.time_in:
            # compare time_in with shift.start_time + grace_period
            scheduled = datetime.combine(att.date, shift.start_time)
            actual = datetime.combine(att.date, att.time_in)
            grace = timedelta(minutes=shift.grace_period or 0)
            if actual <= scheduled + grace:
                att.status_in = "Presente"
            else:
                att.status_in = "Retardo"

    db.add(att)
    db.commit()
    db.refresh(att)
    return att
