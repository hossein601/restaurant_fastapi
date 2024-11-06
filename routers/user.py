# user_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.base import get_db
from dependencies import get_current_user
from models import User
from schemas.user import UserResponse, UpdateProfile, UserUpdate, UpdateWalletResponse, UpdateWalletRequest

user_router = APIRouter()

@user_router.put("/users/profile", response_model=UserResponse)
def update_user_profile(profile_data: UpdateProfile, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.name = profile_data.name
    current_user.address = profile_data.address
    db.commit()
    db.refresh(current_user)
    return current_user

@user_router.put("/users/update_wallet", response_model=UpdateWalletResponse)
def increase_wallet(wallet_data:UpdateWalletRequest , db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    current_user.wallet += wallet_data.wallet
    db.commit()
    db.refresh(current_user)
    return {"wallet": current_user.wallet}

@user_router.put("/users/decrease_wallet", response_model=UpdateWalletResponse)

def decrease_wallet(wallet_data:UpdateWalletRequest, db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    if current_user.wallet > wallet_data.wallet:
        current_user.wallet -= wallet_data.wallet
        db.commit()
        db.refresh(current_user)
        return {"wallet": current_user.wallet}
    return f"There is not enough money to decrease this wallet"





