# app/crud/departments.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate

def get_department(db: Session, dept_id: int) -> Optional[Department]:
    return db.query(Department).filter(Department.id == dept_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 100) -> List[Department]:
    return db.query(Department).offset(skip).limit(limit).all()

def create_department(db: Session, payload: DepartmentCreate) -> Department:
    d = Department(name=payload.name, manager_id=payload.manager_id)
    db.add(d); db.commit(); db.refresh(d)
    return d

def update_department(db: Session, dept: Department, payload: DepartmentUpdate) -> Department:
    data = payload.dict(exclude_unset=True)
    for k,v in data.items():
        setattr(dept, k, v)
    db.add(dept); db.commit(); db.refresh(dept)
    return dept

def delete_department(db: Session, dept: Department):
    db.delete(dept); db.commit()
