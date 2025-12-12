# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --------------------------------------------------------------------
# CONFIGURACIÓN DE LA BASE DE DATOS
# Cambia esta URL por la que uses: MySQL, PostgreSQL o SQLite
# --------------------------------------------------------------------

# Ejemplo SQLite:
DATABASE_URL = "sqlite:///./attendance.db"

# Ejemplo MySQL:
# DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/attendance_db"

# Ejemplo PostgreSQL:
# DATABASE_URL = "postgresql://user:password@localhost:5432/attendance_db"

# --------------------------------------------------------------------
# CREACIÓN DEL MOTOR (ENGINE)
# --------------------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# --------------------------------------------------------------------
# CREACIÓN DE SessionLocal
# --------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --------------------------------------------------------------------
# BASE DEL ORM
# --------------------------------------------------------------------
Base = declarative_base()
