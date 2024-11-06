# models/order_item.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True,default=uuid.uuid4)
    quantity = Column(Integer, nullable=False)

    order = relationship('Order', back_populates='order_items')
    item = relationship('Item', back_populates='order_items')
    order_id = Column(Integer, ForeignKey('orders.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
