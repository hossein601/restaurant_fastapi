from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from config import setting

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=setting.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, setting.secret_key, algorithm=setting.algorithm)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, setting.secret_key, algorithms=[setting.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token is invalid or expired")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token is invalid")
