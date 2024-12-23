
from pydantic import  ConfigDict
from pydantic import BaseModel
from typing import  List

class BasketResponseItem(BaseModel):
    item_id: int
    quantity: int

    class Config:
        orm_mode = True

class BasketResponse(BaseModel):
    item_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class BasketCreateItem(BaseModel):
    item_id:int
    add:bool



    class Config:
        orm_mode = True

class BasketItemResponse(BaseModel):
    items: List[BasketResponse]

    class Config:
        model_config = ConfigDict(from_attributes=True)
