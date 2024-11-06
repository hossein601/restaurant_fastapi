from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base
import uuid

class Staff(Base):
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True,default=uuid.uuid4)
    phone_number = Column(String,unique=True, index=True)
    name = Column(String)
    position = Column(String, nullable=False)

    orders = relationship('Order', back_populates='staff')
    reservations = relationship('Reserve', back_populates='staff')