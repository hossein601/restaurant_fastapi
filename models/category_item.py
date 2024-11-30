from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from models.time_record import TimeRecord

class CategoryItem(TimeRecord, Base):
    __tablename__ = 'category_item'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    item_category = relationship('Item', back_populates='category')

    categories = relationship('Category', back_populates='item')
