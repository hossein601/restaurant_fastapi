from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base
from models.time_record import TimeRecord



class Order(TimeRecord, Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String, nullable=False)
    phone_number = Column(String(15), nullable=False)
    address = Column(String, nullable=False)
    total_price = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey('user.id'))
    staff_id = Column(Integer, ForeignKey('staff.id'))

    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')
    staff = relationship('Staff', back_populates='orders')

