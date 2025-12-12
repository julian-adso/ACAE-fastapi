# app/crud/users.py
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud.utils import hash_password, verify_password

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(
        username=user_in.username,
        document=user_in.document,
        phone=user_in.phone,
        email=user_in.email,
        role=user_in.role or "user",
        horario=user_in.horario,
        department_id=user_in.department_id,
        position_id=user_in.position_id,
        qr_path=user_in.qr_path,
        is_active=user_in.is_active if user_in.is_active is not None else True
    )
    user.password_hash = hash_password(user_in.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user: User, updates: UserUpdate) -> User:
    data: Dict[str, Any] = updates.dict(exclude_unset=True)
    if "password" in data:
        user.password_hash = hash_password(data.pop("password"))
    for field, value in data.items():
        setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def soft_delete_user(db: Session, user: User) -> User:
    user.is_active = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    ok = verify_password(user.password_hash, password, legacy_hash=getattr(user, "legacy_password_hash", None), legacy_algo=getattr(user, "legacy_hash_algorithm", None), db=db, user_obj=user)
    return user if ok else None
