from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date
from ..db.database import Base

# holidays
class Holiday(Base):
    __tablename__ = "holidays"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, unique=True, nullable=False)
    name = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
