from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List


class ItemCreate(BaseModel):
    name: str
    description: Optional[str]
    price: int
    stock: int

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: int
    stock: int

    class Config:
        orm_mode = True

class ItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    stock: Optional[int]


class ItemInfo(BaseModel):
    id:int
    name: str
    price: int
    description: str
    stock: int

    class Config:
        orm_mode = True

class ItemInfoResponse(BaseModel):
    items: List[ItemInfo]

    class Config:
        orm_mode = True

