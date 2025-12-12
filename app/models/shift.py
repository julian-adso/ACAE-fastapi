from datetime import datetime
from sqlalchemy import Column, Time, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..db.database import Base

# shift
class Shift(Base):
    __tablename__ = "shifts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    grace_period = Column(Integer, default=10)  # minutos
    created_at = Column(DateTime, default=datetime.utcnow)
    attendances = relationship('Attendance', back_populates='shift')