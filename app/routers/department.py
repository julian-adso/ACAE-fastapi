# app/routers/departments.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app import deps
from app.crud import department as crud_depts
from app.schemas.department import DepartmentCreate, DepartmentRead, DepartmentUpdate

router = APIRouter(prefix="/departments", tags=["departments"])

@router.post("/", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
def create_department(payload: DepartmentCreate, db: Session = Depends(deps.get_db)):
    return crud_depts.create_department(db, payload)

@router.get("/", response_model=List[DepartmentRead])
def list_departments(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_depts.get_departments(db, skip=skip, limit=limit)

@router.get("/{dept_id}", response_model=DepartmentRead)
def get_department(dept_id: int, db: Session = Depends(deps.get_db)):
    d = crud_depts.get_department(db, dept_id)
    if not d:
        raise HTTPException(status_code=404, detail="department not found")
    return d

@router.patch("/{dept_id}", response_model=DepartmentRead)
def patch_department(dept_id: int, payload: DepartmentUpdate, db: Session = Depends(deps.get_db)):
    d = crud_depts.get_department(db, dept_id)
    if not d:
        raise HTTPException(status_code=404, detail="department not found")
    return crud_depts.update_department(db, d, payload)

@router.delete("/{dept_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(dept_id: int, db: Session = Depends(deps.get_db)):
    d = crud_depts.get_department(db, dept_id)
    if not d:
        raise HTTPException(status_code=404, detail="department not found")
    crud_depts.delete_department(db, d)
    return
