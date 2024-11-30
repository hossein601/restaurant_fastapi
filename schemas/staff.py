from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional
from schemas.item import ItemResponse

class StaffResponse(BaseModel):
    id:int
    phone_number: str
    name:str
    position:str
    created_time: datetime

class StaffCreate(BaseModel):
    phone_number: str
    name: str
    position:str

class StaffUpdate(BaseModel):
    name: Optional[str]
    position: Optional[str]


