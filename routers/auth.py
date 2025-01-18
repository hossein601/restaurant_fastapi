from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User, Basket
from schemas.user import UserSignin, UserLogin
from auth_token import create_access_token
from database.base import get_db
from passlib.hash import bcrypt
from fastapi import Header
auth_router = APIRouter()

@auth_router.post("/signin", status_code=status.HTTP_201_CREATED)
def create_user(user: UserSignin, db: Session = Depends(get_db),guest_user_id: int| None= Header(default=None)):
    existing_user = db.query(User).filter(User.phone_number == user.phone_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone Number already exists")

    hashed_password = bcrypt.hash(user.password)
    new_user = User(phone_number=user.phone_number, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    if guest_user_id:
        guest_user_basket = db.query(Basket).filter(Basket.guest_user_id == guest_user_id).one_or_none()
        guest_user_basket.user_id = new_user.id
        db.commit()

    db.refresh(new_user)
    access_token = create_access_token(data={"sub": str(new_user.id)}, role=new_user.role)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }

@auth_router.post("/login")
def login(user_log: UserLogin, db: Session = Depends(get_db),guest_user_id: int| None= Header(default=None)):
    user = db.query(User).filter(User.phone_number == user_log.phone_number).first()
    if not user or not user.verify_password(user_log.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")
    if guest_user_id:
        guest_user_basket = db.query(Basket).filter(Basket.guest_user_id == guest_user_id).one_or_none()
        guest_user_basket.user_id = user.id
        db.commit()
        db.refresh(guest_user_basket)


    access_token = create_access_token(data={"sub": str(user.id)}, role=user.role)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }