from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from models.time_record import TimeRecord


class Basket(TimeRecord, Base):
    __tablename__ = 'basket'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='basket')
    basket_items = relationship('BasketItem', back_populates='baskets')