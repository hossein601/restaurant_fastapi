from datetime import datetime
from http.client import HTTPException
from typing import Any
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional, List
from fastapi import HTTPException


class ItemCreate(BaseModel):
    name: str = Field(title="The name of the item", max_length=30)
    description: str= Field(default="",description=" description of the item", max_length=100)
    price: int = Field(le=10000, gt=0, description="The price must be greater than zero")
    stock: int = Field(le=10000, gt=0, description="The stock must be greater than zero")
    max_amount: int = Field(le=10000, gt=0, description="The max_amount must be greater than zero")

    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data: Any):
        if isinstance(data, dict):
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            stock = data.get('stock')
            max_amount = data.get('max_amount')

            if not isinstance(name, str) or len(name)>30 or len(name)<0:
                raise HTTPException(status_code=400, detail="name should be string and length more than 30 characters")

            if not isinstance(description, str) or len(description)>100 or len(description)<0:
                raise HTTPException(status_code=400, detail="description should be string and length more than 100 characters")

            if not isinstance(price, int) or price>10000 or price<0:
                raise HTTPException(status_code=400, detail="price should be integer and less than 10000 characters")

            if not isinstance(stock, int) or stock>10000 or stock<0:
                raise HTTPException(status_code=400, detail="stock should be integer and less than 10000 characters")

            if not isinstance(max_amount, int) or max_amount>10000 or max_amount<0:
                raise HTTPException(status_code=400, detail="max_amount should be integer and less than 10000 characters")
        return data

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: int
    stock: int
    created_time: datetime
    max_amount: int

    class Config:
        orm_mode = True

class ItemUpdate(BaseModel):
    name: Optional[str]=Field(default=None, title="The name of the item", max_length=30)
    description: Optional[str]=Field(default=None, title="The description of the item", max_length=300)
    price: Optional[int]=Field(default= 0,le=10000,gt=0, description="The price must be greater than zero")
    stock: Optional[int]=Field(default= 0,le=10000,gt=0, description="The stock must be greater than zero")
    max_amount: Optional[int]=Field(default= 0,le=10000,gt=0, description="The max_amount must be greater than zero")

class ItemInfo(BaseModel):
    id:int
    name: str
    price: int
    description: str
    stock: int
    max_amount: int

    model_config = ConfigDict(from_attributes=True)

class ItemInfoResponse(BaseModel):
    items: List[ItemInfo]

    class Config:
        orm_mode = True

class GetItemFilter(BaseModel):
    item_id:Optional[int]
    category_id:Optional[int]
    price:Optional[int]
    description:Optional[str]
    stock:Optional[int]




