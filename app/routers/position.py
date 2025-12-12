# app/routers/positions.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app import deps
from app.crud import position as crud_positions
from app.schemas.position import PositionCreate, PositionRead, PositionUpdate

router = APIRouter(prefix="/positions", tags=["positions"])

@router.post("/", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
def create_position(payload: PositionCreate, db: Session = Depends(deps.get_db)):
    return crud_positions.create_position(db, payload)

@router.get("/", response_model=List[PositionRead])
def list_positions(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_positions.get_positions(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=PositionRead)
def get_position(id: int, db: Session = Depends(deps.get_db)):
    pos = crud_positions.get_position(db, id)
    if not pos:
        raise HTTPException(status_code=404, detail="position not found")
    return pos

@router.patch("/{id}", response_model=PositionRead)
def patch_position(id: int, payload: PositionUpdate, db: Session = Depends(deps.get_db)):
    pos = crud_positions.get_position(db, id)
    if not pos:
        raise HTTPException(status_code=404, detail="position not found")
    return crud_positions.update_position(db, pos, payload)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_position(id: int, db: Session = Depends(deps.get_db)):
    pos = crud_positions.get_position(db, id)
    if not pos:
        raise HTTPException(status_code=404, detail="position not found")
    crud_positions.delete_position(db, pos)
    return
