from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from database.base import Base
from models.time_record import TimeRecord

class WalletHistory(TimeRecord, Base):
    __tablename__ = 'wallet_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_time = Column(DateTime, default=datetime.utcnow)
    type = Column(String, nullable=True)
    old_balance = Column(Integer, nullable=False)
    new_balance = Column(Integer, nullable=False)

    @hybrid_property
    def tranactions(self):
        return self.new_balance - self.old_balance

    @tranactions.expression
    def tranactions(cls):
        return cls.new_balance - cls.old_balance

    user = relationship('User', back_populates='wallet_history')




