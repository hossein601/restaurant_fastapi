from typing import List, Any
from pydantic import BaseModel, Field, model_validator
from fastapi import HTTPException


class ItemInCategory(BaseModel):
    id: int
    name: str=Field(default=None, title="The name of the Category", max_length=30)
    price: int=Field(default= 0,le=10000,gt=0, description="The price must be greater than zero")
    stock: int=Field(default= 0,le=10000,gt=0, description="The stock must be greater than zero")

    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data: Any):
        if isinstance(data, dict):
            name = data.get('name')
            description = data.get('price')
            stock = data.get('stock')

            if not isinstance(name, str) or len(name)>30 or len(name)<1:
                raise HTTPException(status_code=400, detail="name should be string")

            if not isinstance(description, str) or len(description)>30 or len(description)<1:
                raise HTTPException(status_code=400, detail="description should be string")
            if not isinstance(stock, int) or stock>10000 or stock<1:
                raise HTTPException(status_code=400, detail="stock should be integer")
        return data


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




