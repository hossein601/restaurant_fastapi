from datetime import datetime
from typing import Optional, Any
from pydantic import Field, model_validator
from pydantic import BaseModel, field_validator
from fastapi import  HTTPException
import re
class UserResponse(BaseModel):
    name:str =Field(default=None, title="The name of the user", max_length=30)
    address:str =Field(default=None, title="The description of the address", max_length=100)
    created_time: datetime

class UserCreate(BaseModel):
    id:str
    name: str=Field(default=None, title="The description of the name", max_length=30)
    address: str=Field(default=None, title="The description of the address", max_length=30)
    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data: Any):
        if isinstance(data, dict):
            name = data.get('name')
            address = data.get('price')
            if not isinstance(name, str):
                raise HTTPException(status_code=400, detail="name should be string")
            if not isinstance(address, str):
                raise HTTPException(status_code=400, detail="description should be string")
        return data

class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, title="The description of the address", max_length=30)
    wallet: Optional[int] =Field(default= 0,le=10000,gt=0, description="The wallet must be greater than zero")
    password: str

    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data: Any):
        if isinstance(data, dict):
            name = data.get('name')
            wallet = data.get('price')
            if not isinstance(name, str):
                raise HTTPException(status_code=400, detail="name should be string")
            if not isinstance(wallet, int):
                raise HTTPException(status_code=400, detail="description should be string")
        return data



class UserLogin(BaseModel):
    phone_number:str
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        rule = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
        if not rule.search(value):
            raise HTTPException(status_code=400, detail="Password in not valid")
        return value

    @field_validator("phone_number")
    def validate_mobile(cls, value):

        rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')

        if not rule.search(value):
            raise HTTPException(status_code=400, detail="Phone number is not valid")
        return value
    class Config:
        orm_mode = True


class UserSignin(BaseModel):
    phone_number: str
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        rule = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
        if not rule.search(value):
            raise HTTPException(status_code=400, detail="Password in not valid")
        return value

    @field_validator("phone_number")
    def validate_mobile(cls ,value):

        rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')

        if not rule.search(value):
            raise HTTPException(status_code=400, detail="Phone number is not valid")
        return value

    class Config:
        orm_mode = True

class UpdateProfile(BaseModel):
    name: str=Field(default=None, title="The description of the name", max_length=30)
    address: str=Field(default=None, title="The description of the address", max_length=30)
    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data: Any):
        if isinstance(data, dict):
            name = data.get('name')
            address = data.get('price')
            if not isinstance(name, str) or len(name)<0 or len(name)<30:
                raise HTTPException(status_code=400, detail="name should be string")
            if not isinstance(address, str):
                raise HTTPException(status_code=400, detail="description should be string")
        return data

class UpdateWalletResponse(BaseModel):
    wallet: int
    created_time:datetime

    class Config:
        orm_mode = True

class UpdateWalletRequest(BaseModel):
    wallet: int


class UserInformation(BaseModel):
    name: Optional[str] = None
    address:Optional[str] = None
    phone_number:str
    wallet:int
    created_time:datetime
    class Config:
        orm_mode = True


