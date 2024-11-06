# schemas/order.py
from pydantic import BaseModel
from typing import List, Optional
from schemas.item import ItemResponse

class OrderItemCreate(BaseModel):
    item_name: str
    quantity: int

class OrderCreate(BaseModel):
    customer_name: str
    phone_number: str
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    item: ItemResponse
    quantity: int


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    phone_number: str
    total_price: Optional[int]
    items: List[OrderItemResponse]


class OrderUpdate(BaseModel):
    item_name: str
    quantity: int
