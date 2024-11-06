from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database.base import Base
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Reserve(Base):
    __tablename__ = 'reservation'

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    name = Column(String, nullable=False)
    count = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    staff_id = Column(Integer, ForeignKey('staff.id'))

    user = relationship('User', back_populates='reservations')
    staff = relationship('Staff', back_populates='reservations')