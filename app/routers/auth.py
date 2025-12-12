# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Body
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Any, Optional
from app import deps
from app.schemas.user import UserCreate, UserRead
from app.schemas.password_reset_token import PasswordResetTokenCreate
from app.crud import user as crud_users
from app.crud import password_reset_token as crud_tokens

router = APIRouter(prefix="/auth", tags=["auth"])

# NOTE: Replace this with your JWT/session implementation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # Placeholder: generate JWT here
    return "ACCESS_TOKEN_PLACEHOLDER"

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(deps.get_db)):
    if crud_users.get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="username already exists")
    if crud_users.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="email already registered")
    user = crud_users.create_user(db, payload)
    return user

@router.post("/login")
def login(form_data: dict = Body(...), db: Session = Depends(deps.get_db)):
    """
    Expects JSON body: {"username": "...", "password": "..."}.
    Consider replacing with OAuth2PasswordRequestForm for standards.
    """
    username = form_data.get("username")
    password = form_data.get("password")
    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username and password required")

    user = crud_users.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # update last_login
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    # create token
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer", "user": UserRead.from_orm(user)}

@router.post("/request-password-reset", status_code=201)
def request_password_reset(payload: dict = Body(...), background_tasks: BackgroundTasks = None, db: Session = Depends(deps.get_db)):
    """
    payload: {"email": "user@example.com"}
    Implement sending email in background_tasks.
    """
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is required")
    user = crud_users.get_user_by_email(db, email)
    if not user:
        # respond success to avoid leaking emails
        return {"msg": "If the email exists, a reset link will be sent."}
    token_obj = crud_tokens.create_reset_token(db, user_id=user.id, expiry_minutes=60)
    # schedule email sending with background_tasks (implement send_reset_email)
    # if background_tasks:
    #     background_tasks.add_task(send_reset_email, user.email, token_obj.token)
    return {"msg": "If the email exists, a reset link will be sent."}

@router.post("/reset-password")
def reset_password(payload: dict = Body(...), db: Session = Depends(deps.get_db)):
    """
    payload: {"token": "<token>", "new_password": "..." }
    """
    token = payload.get("token")
    new_password = payload.get("new_password")
    if not token or not new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="token and new_password are required")

    token_obj = crud_tokens.get_reset_token(db, token)
    if not token_obj:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    # validate expiry
    if token_obj.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")
    # load user and change password
    user = crud_users.get_user(db, token_obj.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # prefer using the user model helper if present, else set password_hash
    if hasattr(user, "set_password"):
        user.set_password(new_password)
    else:
        from app.crud.utils import hash_password
        user.password_hash = hash_password(new_password)
    db.add(user)
    # mark token used
    crud_tokens.mark_token_used(db, token_obj)
    db.commit()
    return {"msg": "Password updated"}
