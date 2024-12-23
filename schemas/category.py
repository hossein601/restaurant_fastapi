from pydantic import BaseModel, Field, model_validator
from typing import List, Any
from fastapi import HTTPException

class CategoryCreate(BaseModel):
    name: str=Field(default=None, title="The name of the Category", max_length=30)
    description: str=Field(default=None, title="The name of the item", max_length=30)

    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data: Any):
        if isinstance(data, dict):
            name = data.get('name')
            description = data.get('description')

            if not isinstance(name, str) or len(name)>30 or len(name)<1:
                raise HTTPException(status_code=400, detail="name should be string")

            if not isinstance(description, str) or len(description)>30 or len(description)<1:
                raise HTTPException(status_code=400, detail="description should be string")
        return data

class CategoryUpdateQuery(BaseModel):
    category_id:str

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
