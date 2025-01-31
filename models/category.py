from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base
from models.time_record import TimeRecord


class Category(TimeRecord, Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=False)

    item = relationship("CategoryItem", back_populates="categories")
