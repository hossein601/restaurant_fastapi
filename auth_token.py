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


def verify_token(token: str):
    try:
        payload = jwt.decode(token, setting.secret_key, algorithms=[setting.algorithm])
        user_id: str = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

        return user_id

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid")
