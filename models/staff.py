from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base
from models.time_record import TimeRecord


class Staff(TimeRecord, Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number=Column(String, nullable=False)
    orders = relationship("Order", back_populates="staff")
    position = Column(String, nullable=False)
