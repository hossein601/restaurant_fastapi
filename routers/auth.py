from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User
from schemas.user import UserSignin, UserLogin
from auth_token import create_access_token
from database.base import get_db
from passlib.hash import bcrypt

auth_router = APIRouter()

@auth_router.post("/auth/signin", status_code=status.HTTP_201_CREATED)
def create_user(user: UserSignin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone_number == user.phone_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    hashed_password = bcrypt.hash(user.password)
    new_user = User(phone_number=user.phone_number, hashed_password=hashed_password)
    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {"message": "User created successfully"}

@auth_router.post("/auth/login")
def login(user_cred: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == user_cred.phone_number).first()
    if not user or not user.verify_password(user_cred.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)}, role=user.role)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }