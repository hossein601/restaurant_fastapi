from datetime import datetime
from typing import List
from pydantic import BaseModel


class ItemInCategory(BaseModel):
    id: int
    name: str
    price: int
    stock: int

    class Config:
        orm_mode = True

class ItemsForCategoryResponse(BaseModel):
    items: List[ItemInCategory]

    class Config:
        orm_mode = True
from typing import List

class CategoryInItem(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

class CategoriesForItemResponse(BaseModel):
    item_id: int
    categories: List[CategoryInItem]

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





