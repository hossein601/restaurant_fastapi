from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base
from models.time_record import TimeRecord


class Staff(TimeRecord, Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(15), nullable=False, unique=True)
    position = Column(String(50), nullable=False)
