from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..db.database import Base

# device
class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    identifier = Column(String(100), unique=True, nullable=False) # serial o mac o nombre
    location = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    attendances = relationship('Attendance', back_populates='device')