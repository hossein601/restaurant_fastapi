from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from database.base import Base
from models.time_record import TimeRecord

class GuestUser(TimeRecord, Base):
    __tablename__ = "guest_user"

    id = Column(Integer, primary_key=True,unique=True)
    guest_basket = relationship("Basket", back_populates="guest_user_relationship")

