from pydantic import BaseModel
from typing import List
from datetime import datetime

class CategoryCreate(BaseModel):
    name: str
    description: str

class CategoryResponse(BaseModel):
    message: str

    class Config:
        arbitrary_types_allowed=True
        orm_mode=True

class CategoryInfo(BaseModel):
    id:int
    name: str
    description: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class CategoryInfoResponse(BaseModel):
    categories: List[CategoryInfo]

    class Config:
        orm_mode = True
