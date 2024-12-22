from datetime import datetime, timedelta
from fastapi import HTTPException, status
import jwt
from jwt import ExpiredSignatureError, PyJWTError
from config import setting


def create_access_token(data: dict, role: str, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    to_encode.update({"role": role, "exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, setting.secret_key, algorithm=setting.algorithm)
    return encoded_jwt
