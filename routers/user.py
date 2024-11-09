# routers/user_router.py
from http.client import responses

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from dependencies import get_current_user, role_checker
from database.base import get_db
from models.user import User, Role
from schemas.user import UserResponse, UpdateProfile, UpdateWalletRequest, UserInformation, CreateAdminRequest, \
    CreateUserRequest, UpdateWalletResponse
import bcrypt

user_router = APIRouter()

@user_router.get("/users_profile", response_model=UserInformation, dependencies=[Depends(role_checker(["user", "admin"]))])
def get_users_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_info = db.query(User).filter(User.id == current_user.id).one_or_none()
    if user_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info

@user_router.put("/users/profile", response_model=UserInformation,dependencies=[Depends(role_checker(["user", "admin"]))])
def update_user_profile(profile_data: UpdateProfile, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.name = profile_data.name
    current_user.address = profile_data.address
    db.commit()

    db.refresh(current_user)
    return current_user

@user_router.put("/users/increase_wallet", response_model=UpdateWalletResponse, dependencies=[Depends(role_checker(["user", "admin"]))])
def increase_wallet(wallet_data: UpdateWalletRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.wallet += wallet_data.wallet
    db.commit()

    db.refresh(current_user)
    return {"wallet": current_user.wallet}
@user_router.put("/users/decrease_wallet", response_model=UpdateWalletResponse, dependencies=[Depends(role_checker(["user", "admin"]))])
def decrease_wallet(wallet_data: UpdateWalletRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.wallet<wallet_data.wallet:
        raise HTTPException(status_code=403, detail="There is not enough money")
    current_user.wallet -= wallet_data.wallet
    db.commit()

    db.refresh(current_user)
    return {"wallet": current_user.wallet}

@user_router.delete("/users/delete_user", dependencies=[Depends(role_checker(["admin"]))])
def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_user = db.query(User).filter(User.id == current_user.id).one_or_none()
    if delete_user:
        db.delete(delete_user)
        db.commit()
        return {"success": True}

    raise HTTPException(status_code=404, detail="User not found")

@user_router.put("/users/create_admin", status_code=status.HTTP_200_OK,)
def create_admin(role: CreateUserRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if role.role not in ["user", "admin"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    current_user.role = role.role
    db.commit()

    db.refresh(current_user)

    return {"success": True}



def authenticate_admin(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == username).first()

    if user is None or not user.verify_password(password) or user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password, or insufficient permissions",
        )

    return user
from fastapi import FastAPI, Depends

app = FastAPI()

@app.post("/admin-login")
def admin_login(username: str, password: str, user: User = Depends(authenticate_admin)):
    # At this point, `user` is a verified admin
    return {"message": f"Welcome, Admin {user.name}!"}
