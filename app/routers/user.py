# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import deps
from app.crud import user as crud_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(deps.get_db)):
    if crud_users.get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="username already exists")
    if crud_users.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="email already registered")
    return crud_users.create_user(db, payload)

@router.get("/", response_model=List[UserRead])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_users.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(deps.get_db)):
    u = crud_users.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="user not found")
    return u

@router.patch("/{user_id}", response_model=UserRead)
def patch_user(user_id: int, payload: UserUpdate, db: Session = Depends(deps.get_db)):
    u = crud_users.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="user not found")
    return crud_users.update_user(db, u, payload)

@router.delete("/{user_id}", response_model=UserRead)
def deactivate_user(user_id: int, db: Session = Depends(deps.get_db)):
    u = crud_users.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="user not found")
    return crud_users.soft_delete_user(db, u)
