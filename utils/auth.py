from datetime import datetime, timedelta
from typing import Union, Any, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from config import setting

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    expires_at = datetime.utcnow() + timedelta(minutes=setting.access_token_expire_minutes)
    to_encode = {"exp": expires_at, "sub": str(subject)}
    return jwt.encode(to_encode, setting.secret_key, setting.algorithm)

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    expires_at = datetime.utcnow() + timedelta(minutes=setting.refresh_token_expire_minutes)
    to_encode = {"exp": expires_at, "sub": str(subject)}
    return jwt.encode(to_encode, setting.refresh_secret_key, setting.algorithm)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
