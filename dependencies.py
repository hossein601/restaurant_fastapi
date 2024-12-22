from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session
from config import setting
from database.base import get_db
from models.user import User
import contextvars

token_auth_scheme = HTTPBearer()

_current_user_cache = contextvars.ContextVar("current_user_cache", default=None)

def get_token_payload(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)) -> dict:

    try:
        payload = jwt.decode(token.credentials, setting.secret_key, algorithms=[setting.algorithm])
        user_id: str = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid")


def get_current_user(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db)
) -> User:

    cached_user = _current_user_cache.get()
    if cached_user:
        return cached_user

    user_id: str = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    _current_user_cache.set(user)

    return user


def role_checker(required_roles: list):
    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return current_user

    return checker
