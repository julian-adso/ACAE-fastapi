# app/deps.py

from sqlalchemy.orm import Session
from app.db.database import SessionLocal

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
