from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session
from config import setting
from database.base import get_db
from models import User

token_auth_scheme = HTTPBearer()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
                     db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token.credentials, setting.secret_key, algorithms=[setting.algorithm])

        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid")
