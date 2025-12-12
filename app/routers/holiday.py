# app/routers/holidays.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app import deps
from app.crud import holiday as crud_holidays
from app.schemas.holiday import HolidayCreate, HolidayRead, HolidayUpdate

router = APIRouter(prefix="/holidays", tags=["holidays"])

@router.post("/", response_model=HolidayRead, status_code=status.HTTP_201_CREATED)
def create_holiday(payload: HolidayCreate, db: Session = Depends(deps.get_db)):
    return crud_holidays.create_holiday(db, payload)

@router.get("/", response_model=List[HolidayRead])
def list_holidays(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_holidays.get_holidays(db, skip=skip, limit=limit)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_holiday(id: int, db: Session = Depends(deps.get_db)):
    h = crud_holidays.get_holiday(db, id)
    if not h:
        raise HTTPException(status_code=404, detail="holiday not found")
    crud_holidays.delete_holiday(db, h)
    return
