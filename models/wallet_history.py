from enum import Enum
from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship
from database.base import Base
from datetime import datetime
from models.time_record import TimeRecord


class Type(Enum):
    increase = 1
    decrease = 2

class WalletHistory(TimeRecord,Base):
    __tablename__ = 'wallet_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_time = Column(DateTime, default=datetime.utcnow)
    type = Column(String, nullable=True)
    old_balance = Column(Float, nullable=False)
    new_balance = Column(Float, nullable=False)

    user = relationship('User', back_populates='wallet_history')
