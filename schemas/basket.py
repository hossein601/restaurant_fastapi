from datetime import datetime

from pydantic import BaseModel
from pydantic import BaseModel
from typing import Optional, List

class BasketResponseItem(BaseModel):
    item_id: int
    quantity: int

    class Config:
        orm_mode = True

class BasketResponse(BaseModel):
    item_id: int
    quantity: int


    class Config:
        orm_mode = True


class BasketCreateItem(BaseModel):
    item_id: int
    quantity: int

    class Config:
        orm_mode = True

class BasketItemResponse(BaseModel):
    items: List[BasketResponse]

    class Config:
        orm_mode = True
