
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_current_user, role_checker
from database.base import get_db
from models.user import User
from schemas.user import  UpdateProfile, UpdateWalletRequest, UserInformation, CreateAdminRequest, \
    UpdateWalletResponse
import bcrypt

user_router = APIRouter()


@user_router.get("/users/", response_model=UserInformation, dependencies=[Depends(role_checker(["user", "admin"]))])
def get_users_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_info = db.query(User).filter(User.id == current_user.id).one_or_none()

    return user_info


@user_router.put("/users/", response_model=UserInformation, dependencies=[Depends(role_checker(["user", "admin"]))])
def update_user_profile(profile_data: UpdateProfile, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    current_user.name = profile_data.name
    current_user.address = profile_data.address
    db.commit()

    db.refresh(current_user)
    return current_user


@user_router.put("/users/increase_wallet", response_model=UpdateWalletResponse,
                 dependencies=[Depends(role_checker(["user", "admin"]))])
def increase_wallet(wallet_data: UpdateWalletRequest, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    current_user.wallet += wallet_data.wallet
    db.commit()

    db.refresh(current_user)
    return {"wallet": current_user.wallet}


@user_router.put("/users/decrease_wallet", response_model=UpdateWalletResponse,
                 dependencies=[Depends(role_checker(["user", "admin"]))])
def decrease_wallet(wallet_data: UpdateWalletRequest, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    if current_user.wallet < wallet_data.wallet:
        raise HTTPException(status_code=403, detail="There is not enough money")
    current_user.wallet -= wallet_data.wallet
    db.commit()

    db.refresh(current_user)
    return {"wallet": current_user.wallet}


@user_router.delete("/users/",status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_checker(["admin","user"]))])
def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_user = db.query(User).filter(User.id == current_user.id).one_or_none()
    db.delete(delete_user)
    db.commit()
    return {"success": True}



