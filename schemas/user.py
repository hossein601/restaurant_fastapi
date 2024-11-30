from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from typing import Literal
from pydantic import BaseModel, Field
from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator
from fastapi import  HTTPException
import re



class UserResponse(BaseModel):
    name:str
    address:str
    created_time: datetime
class UserCreate(BaseModel):
    id:str
    name: str
    address: str
class UserUpdate(BaseModel):
    name: Optional[str] = None
    wallet: Optional[int] = None
    password: str

    class Config:
        orm_mode = True
class UserOut(BaseModel):
    name: Optional[str] = None
    phone_number:str
    wallet: int

    class Config:
        orm_mode = True

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
class Token(BaseModel):
    access_token: str
    token_type: str

class UpdateProfile(BaseModel):
    name: str
    address: str

    class Config:
        orm_mode = True
class UpdateWalletResponse(BaseModel):
    wallet: int
    class Config:
        orm_mode = True

class UpdateWalletRequest(BaseModel):
    wallet: int

class DeleteUserResponse(BaseModel):
    id:int

class UserRequestProfile(BaseModel):
    id:int

class UserInformation(BaseModel):
    name: Optional[str] = None
    address:Optional[str] = None
    phone_number:str
    wallet:int
    class Config:
        orm_mode = True

class CreateUserRequest(BaseModel):
    role: Literal['user', 'admin']

    class Config:
        orm_mode = True

class CreateAdminRequest(BaseModel):
    name: str
    phone_number:str

    class Config:
        orm_mode = True

