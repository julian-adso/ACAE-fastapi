# app/routers/attendance.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app import deps
from app.crud import attendance as crud_att
from app.crud import correction as crud_corr
from app.schemas.attendance import AttendanceRead, AttendanceCreate, AttendanceUpdate
from app.schemas.attendance_correction import AttendanceCorrectionCreate, AttendanceCorrectionRead

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/clock", response_model=AttendanceRead)
def clock_me(user_id: int = Body(...), timestamp: Optional[datetime] = Body(None), device_id: Optional[int] = Body(None), db: Session = Depends(deps.get_db)):
    ts = timestamp or datetime.utcnow()
    att = crud_att.clock_in_out(db=db, user_id=user_id, timestamp=ts, device_id=device_id)
    return att

@router.get("/user/{user_id}", response_model=List[AttendanceRead])
def list_user_attendance(user_id: int, from_date: Optional[str] = None, to_date: Optional[str] = None, db: Session = Depends(deps.get_db)):
    from datetime import datetime as dt
    fd = dt.fromisoformat(from_date).date() if from_date else None
    td = dt.fromisoformat(to_date).date() if to_date else None
    return crud_att.get_attendances_for_user(db, user_id=user_id, from_date=fd, to_date=td)

@router.post("/create", response_model=AttendanceRead, status_code=status.HTTP_201_CREATED)
def create_attendance(payload: AttendanceCreate, db: Session = Depends(deps.get_db)):
    return crud_att.create_attendance(db, payload)

@router.patch("/{id}", response_model=AttendanceRead)
def patch_attendance(id: int, payload: AttendanceUpdate, db: Session = Depends(deps.get_db)):
    att = crud_att.get_attendance(db, id)
    if not att:
        raise HTTPException(status_code=404, detail="attendance not found")
    return crud_att.update_attendance(db, att, payload)

# Corrections
@router.post("/corrections", response_model=AttendanceCorrectionRead, status_code=status.HTTP_201_CREATED)
def request_correction(payload: AttendanceCorrectionCreate, db: Session = Depends(deps.get_db)):
    return crud_corr.request_correction(db, payload)

@router.patch("/corrections/{id}", response_model=AttendanceCorrectionRead)
def review_correction(id: int, payload: dict, db: Session = Depends(deps.get_db)):
    corr = crud_corr.get_correction(db, id)
    if not corr:
        raise HTTPException(status_code=404, detail="correction not found")
    reviewer_id = payload.get("reviewed_by")
    approve = payload.get("approve", False)
    new_values = payload.get("new_values")
    return crud_corr.review_correction(db, corr, reviewer_id, approve, new_values)
