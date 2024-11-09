from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from typing import Literal


class UserResponse(BaseModel):
    name:str
    address:str

class UserCreate(BaseModel):
    id:str
    name: str
    address: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    wallet: Optional[int] = None
    password: Optional[str] = None

class UserOut(BaseModel):
    name: Optional[str] = None
    phone_number: str
    wallet: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    phone_number: str
    password: str

class UserSignin(BaseModel):
    phone_number: str
    password: str

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
    name:str
    address:str
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
    phone_number: str

