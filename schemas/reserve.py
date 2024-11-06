from pydantic import BaseModel
from typing import List, Optional
from schemas.item import ItemResponse

class ReserveResponse(BaseModel):
    id:int
    name:str
    count:int
class ReserveCreate(BaseModel):
    name:str
    count:int

class ReserveUpdate(BaseModel):
    name:str
    count:int





