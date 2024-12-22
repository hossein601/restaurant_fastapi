from datetime import datetime

from pydantic import BaseModel,Field
from typing import List, Optional
from schemas.item import ItemResponse

class OrderItemCreate(BaseModel):
    item_name: str=Field(default=None, title="The name of the staff", max_length=30)
    quantity: int=Field(default= 0,le=100,gt=0, description="The quantity must be greater than zero")


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    total_price: int
    created_time: datetime
    phone_number:str
    customer_name:str
    user_id:int


class OrderResponse(BaseModel):
    items: List[OrderItemCreate]

    total_price: Optional[int]
    items: List[OrderItemResponse]

class OrderUpdate(BaseModel):
    items: List[OrderItemCreate]

class OrderGetResponse(BaseModel):
    total_price:int
    item_name:str

class OrderResponseGet(BaseModel):
    item_id:int
    quantity:int

class OrderGetResponsePaginate(BaseModel):
    order_id:int
    customer_name:str
    phone_number:str
    total_price:int
    items: List[OrderResponseGet]







