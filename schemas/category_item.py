from datetime import datetime
from typing import List
from pydantic import BaseModel,Field


class ItemInCategory(BaseModel):
    id: int
    name: str=Field(default=None, title="The name of the Category", max_length=30)
    price: int=Field(default= 0,le=10000,gt=0, description="The price must be greater than zero")
    stock: int=Field(default= 0,le=10000,gt=0, description="The stock must be greater than zero")

    class Config:
        orm_mode = True


class CategoryItemResponse(BaseModel):
    id: int
    name: str
    price: int
    stock: int

    class Config:
        orm_mode = True

class CategoryItemListResponse(BaseModel):
    category_items : List[CategoryItemResponse]
    class Config:
        orm_mode = True


class CategoryItemUpdate(BaseModel):
    category_id:int
    item_id: int
    class  Config:
        arbitrary_types_allowed = True
class CategoryItemUpdateOut(BaseModel):
    category_id:int
    class  Config:
        arbitrary_types_allowed = True

class Category_item_to_category(BaseModel):
    item_id: int
    category_id: int
    class Config:
        orm_mode = True

class Category_assign_item(BaseModel):
    item_id: int
    class  Config:
        arbitrary_types_allowed = True




