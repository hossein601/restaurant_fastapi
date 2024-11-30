from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from models.time_record import TimeRecord


class BasketItem(TimeRecord, Base):
    __tablename__ = 'basket_item'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    basket_id = Column(Integer, ForeignKey('basket.id'))
    item_id = Column(Integer, ForeignKey('item.id'))

    baskets = relationship('Basket', back_populates='basket_items')
    items = relationship('Item', back_populates='basket')
