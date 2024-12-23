from datetime import datetime
import re

from pydantic import BaseModel, Field, model_validator, field_validator
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

    @field_validator("phone_number")
    def validate_mobile(cls, value):
        rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')

        if not rule.search(value):
            raise HTTPException(status_code=400, detail="Phone number is not valid")
        return value

    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data: Any):
        if isinstance(data, dict):
            name = data.get('name')
            position = data.get('position')
            phone_number = data.get('phone_number')

            if not isinstance(name, str) or len(name)>30 or len(name)<0:
                raise HTTPException(status_code=400, detail="name should be string and length less than 30 characters")

            if not isinstance(position, str) or len(position)>100 or len(position)<0:
                raise HTTPException(status_code=400, detail="position should be string and length less than 100 characters")

            if not isinstance(phone_number, str):
                raise HTTPException(status_code=400, detail="phone_number should be string and length less than 30 characters")

        return data

class StaffUpdate(BaseModel):
    name: Optional[str]
    position: Optional[str]
    updated_time: datetime
    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data: Any):
        if isinstance(data, dict):
            name = data.get('name')
            position = data.get('position')
            if not isinstance(name, str) or len(name)>30 or len(name)<0:
                raise HTTPException(status_code=400, detail="name should be string and length less than 30 characters")

            if not isinstance(position, str) or len(position)>100 or len(position)<0:
                raise HTTPException(status_code=400, detail="position should be string and length less than 100 characters")

        return data




