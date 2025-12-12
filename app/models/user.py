# app/models/user.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..db.database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)            # antes idUser
    username = Column(String(50), unique=True, nullable=False)           # antes usernameUser
    password_hash = Column(String(255), nullable=False)                  # antes passwordUser (reemplazar SHA1)
    legacy_password_hash = Column(String(255), nullable=True)            # opcional: para migración desde SHA1
    legacy_hash_algorithm = Column(String(50), nullable=True)            # e.g. 'sha1'
    document = Column(String(100), nullable=False)                       # antes documentUser
    phone = Column(String(15), nullable=True)                            # antes phoneUser (puede ser nullable)
    email = Column(String(100), unique=True, nullable=False)             # antes emailUser
    role = Column(Enum('user','admin','super', name='role_enum'), default='user', nullable=False)
    horario = Column(Enum('Mañana','Tarde','Noche', name='horario_enum'), nullable=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=True)
    qr_path = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    attendances = relationship('Attendance', back_populates='user', lazy='dynamic')
    department = relationship('Department', back_populates='users', foreign_keys=[department_id])
    position = relationship('Position', back_populates='users', foreign_keys=[position_id])

    # password helpers
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        # Revisa PBKDF2 (werkzeug) primero
        try:
            if check_password_hash(self.password_hash, password):
                return True
        except Exception:
            pass
        # fallback legacy (ej. SHA1) y si coincide, rehash y guardar
        import hashlib
        if self.legacy_password_hash and self.legacy_hash_algorithm == 'sha1':
            if self.legacy_password_hash == hashlib.sha1(password.encode('utf-8')).hexdigest():
                # upgrade
                self.set_password(password)
                self.legacy_password_hash = None
                self.legacy_hash_algorithm = None
                return True
        return False
