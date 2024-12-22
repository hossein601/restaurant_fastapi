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
    name: str=Field(default=None, title="The name of the staff", max_length=30)
    position:str=Field(default=None, title="The position of the staff", max_length=30)
    created_time: datetime

    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data: Any):
        if isinstance(data, dict):
            name = data.get('name')
            position = data.get('description')
            if not isinstance(name, str):
                raise HTTPException(status_code=400, detail="name should be string")
            if not isinstance(position, str):
                raise HTTPException(status_code=400, detail="description should be string")
        return data

class StaffUpdate(BaseModel):
    name: Optional[str]=Field(default=None, title="The name of the staff", max_length=30)
    position: Optional[str]=Field(default=None, title="The position of the staff", max_length=30)
    updated_time: datetime

    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data: Any):
        if isinstance(data, dict):
            name = data.get('name')
            position = data.get('description')
            if not isinstance(name, str):
                raise HTTPException(status_code=400, detail="name should be string")
            if not isinstance(position, str):
                raise HTTPException(status_code=400, detail="description should be string")
        return data


