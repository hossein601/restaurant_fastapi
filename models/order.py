# models/order.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base
from models.time_record import TimeRecord
from models.user import User
from models.staff import Staff

class Order(TimeRecord, Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String, nullable=False)
    phone_number = Column(String(15), nullable=False)
    total_price = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    staff_id = Column(Integer, ForeignKey('staff.id'))

    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')
    staff = relationship('Staff', back_populates='orders')

    def calculate_total_price(self):
        total = 0
        for item in self.order_items:
            total += item.item.price * item.quantity

        self.total_price = total
        return total
