from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from database.base import Base


class TimeRecord(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_time = Column(DateTime, default=datetime.utcnow)
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
