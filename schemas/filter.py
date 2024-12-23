from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from openai import BaseModel

from models import Item


class ItemFilter(Filter):
    id: Optional[int]=None
    price: Optional[int]=None
    description: Optional[str]=None

    class Constants(Filter.Constants):
        model = Item


class CategoryFilter(BaseModel):
    category_id: Optional[int]=None
    category_name: Optional[str]=None

class FilterResponse(BaseModel):
    id:int
    price:int
    max_amount:int
    stock:int
