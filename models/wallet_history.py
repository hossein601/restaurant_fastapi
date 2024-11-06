# from enum import Enum
# from sqlalchemy import Column, Integer, ForeignKey, Float,String
# from sqlalchemy.orm import relationship
# from database.base import Base
# from sqlalchemy import Column, func, text, Datetime, Integer
# from datetime import datetime
#
#
# class Type(Enum):
#     increase = 1
#     decrease = 2
#
# class WalletHistory( Base):
#     __tablename__ = 'wallet_history'
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(String, ForeignKey('users.id'), nullable=False)
#     created_time = Column(Datetime, default=datetime.datetime.utcnow)
#
#     type = Column(Enum(Type) , nullable=True)
#     old_balance = Column(Float, nullable=False)
#     new_balance = Column(Float, nullable=False)
#
#     user = relationship('user', back_populates='wallet_history')