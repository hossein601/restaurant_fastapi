# models/order.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base
from sqlalchemy.dialects.postgresql import UUID

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String, nullable=False)
    phone_number = Column(String(15), nullable=False)
    total_price = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')
    staff_id = Column(Integer, ForeignKey('staff.id'))
    staff = relationship('Staff', back_populates='orders')

    def calculate_total_price(self):
        total = 0
        for item in self.order_items:
            total += item.item.price * item.quantity

        self.total_price = total
        return total
