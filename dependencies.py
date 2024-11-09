from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session
from config import setting
from database.base import get_db
from models.user import User

token_auth_scheme = HTTPBearer()



def get_current_user(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
                     db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token.credentials, setting.secret_key, algorithms=[setting.algorithm])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role mismatch")

        return user

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid")


def role_checker(required_role:list):
    def checker(current_user=Depends(get_current_user)):
        if current_user.role not in required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denie "
            )
        return current_user
    return checker

