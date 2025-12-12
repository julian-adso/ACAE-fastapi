from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Enum, Text, ForeignKey
from ..db.database import Base

# attendance_corrections
class AttendanceCorrection(Base):
    __tablename__ = "attendance_corrections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    attendance_id = Column(Integer, ForeignKey('attendance.id'), nullable=False)
    requester_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reason = Column(Text, nullable=False)
    requested_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum('pending','approved','rejected', name='correction_status'), default='pending')
    reviewed_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)