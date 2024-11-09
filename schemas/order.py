from pydantic import BaseModel
from typing import List, Optional
from schemas.item import ItemResponse

class OrderItemCreate(BaseModel):
    item_name: str
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    item: ItemResponse
    quantity: int

class OrderResponse(BaseModel):
    id: int
    staff_id :int
    items: List[OrderItemCreate]

    total_price: Optional[int]
    items: List[OrderItemResponse]

class OrderUpdate(BaseModel):
    items: List[OrderItemCreate]
