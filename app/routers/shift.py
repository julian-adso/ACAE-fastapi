# app/routers/shifts.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app import deps
from app.crud import shift as crud_shifts
from app.schemas.shift import ShiftCreate, ShiftRead, ShiftUpdate

router = APIRouter(prefix="/shifts", tags=["shifts"])

@router.post("/", response_model=ShiftRead, status_code=status.HTTP_201_CREATED)
def create_shift(payload: ShiftCreate, db: Session = Depends(deps.get_db)):
    return crud_shifts.create_shift(db, payload)

@router.get("/", response_model=List[ShiftRead])
def list_shifts(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_shifts.get_shifts(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=ShiftRead)
def get_shift(id: int, db: Session = Depends(deps.get_db)):
    s = crud_shifts.get_shift(db, id)
    if not s:
        raise HTTPException(status_code=404, detail="shift not found")
    return s

@router.patch("/{id}", response_model=ShiftRead)
def patch_shift(id: int, payload: ShiftUpdate, db: Session = Depends(deps.get_db)):
    s = crud_shifts.get_shift(db, id)
    if not s:
        raise HTTPException(status_code=404, detail="shift not found")
    return crud_shifts.update_shift(db, s, payload)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shift(id: int, db: Session = Depends(deps.get_db)):
    s = crud_shifts.get_shift(db, id)
    if not s:
        raise HTTPException(status_code=404, detail="shift not found")
    crud_shifts.delete_shift(db, s)
    return
