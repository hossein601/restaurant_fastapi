from datetime import datetime

from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Any
from fastapi import HTTPException
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
    created_time: datetime


class StaffUpdate(BaseModel):
    name: Optional[str]
    position: Optional[str]
    updated_time: datetime




