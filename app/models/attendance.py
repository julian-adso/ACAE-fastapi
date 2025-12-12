# app/models/attendance.py
from datetime import datetime
from sqlalchemy import Column, Integer, Date, Time, Enum, Text, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from ..db.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)                 # fecha del registro (día)
    time_in = Column(Time, nullable=True)
    time_out = Column(Time, nullable=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=True)  # dispositivo que registró
    location = Column(String(200), nullable=True)       # opcional: ubicación del scanner/QR
    status_in = Column(Enum('Presente','Retardo','Ausente', name='status_enum'), nullable=True)
    status_out = Column(Enum('Presente','Temprano','Normal','Ausente', name='status_out_enum'), nullable=True)
    motivo_in = Column(Text, nullable=True)
    motivo_out = Column(Text, nullable=True)
    worked_hours = Column(Float, nullable=True)         # calculado (time_out - time_in) - breaks
    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='attendances')
    device = relationship('Device', back_populates='attendances')
    shift = relationship('Shift', back_populates='attendances')
