from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base
from models.time_record import TimeRecord


class Item(TimeRecord, Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)

    order_items = relationship('OrderItem', back_populates='item')
    basket = relationship('BasketItem', back_populates='items')

    category  = relationship('CategoryItem', back_populates='item_category')

    def decrease_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
        else:
            raise ValueError('Not enough stock.')
