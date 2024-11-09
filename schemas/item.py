from pydantic import BaseModel
from typing import Optional

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
