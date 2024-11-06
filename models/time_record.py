# from datetime import datetime
# from sqlalchemy import Column, func, text, Datetime, Integer
# from database.base import Base
#
#
# class TimeRecord(Base):
#     __tablename__ = 'time_record'
#
#     id = Column(Integer, primary_key=True)
#     created_time = Column(Datetime, default=datetime.datetime.utcnow)
#     updated_time = Column(Datetime, default=datetime.datetime.utcnow, onupdate=datetime.utcnow)