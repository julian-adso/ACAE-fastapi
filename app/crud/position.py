# app/crud/positions.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.position import Position
from app.schemas.position import PositionCreate, PositionUpdate

def get_position(db: Session, id: int) -> Optional[Position]:
    return db.query(Position).filter(Position.id == id).first()

def get_positions(db: Session, skip: int = 0, limit: int = 100) -> List[Position]:
    return db.query(Position).offset(skip).limit(limit).all()

def create_position(db: Session, payload: PositionCreate) -> Position:
    p = Position(name=payload.name)
    db.add(p); db.commit(); db.refresh(p)
    return p

def update_position(db: Session, pos: Position, payload: PositionUpdate) -> Position:
    data = payload.dict(exclude_unset=True)
    for k,v in data.items():
        setattr(pos, k, v)
    db.add(pos); db.commit(); db.refresh(pos)
    return pos

def delete_position(db: Session, pos: Position):
    db.delete(pos); db.commit()
