# routers/order_router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.reserve import Reserve
from models.staff import Staff
from models.item import Item
from models.user import User
from schemas.order import OrderCreate, OrderResponse, OrderUpdate
from database.base import get_db
from schemas.reserve import ReserveResponse, ReserveCreate, ReserveUpdate
from schemas.staff import StaffResponse, StaffCreate, StaffUpdate

reserve_router = APIRouter()

@reserve_router.post("/reserve",response_model=ReserveResponse, status_code=status.HTTP_201_CREATED)
def create_reserve(reserve_data :ReserveCreate,db:Session=Depends(get_db)):
    new_reserve = Reserve(**reserve_data.dict())
    db.add(new_reserve)
    db.commit()
    db.refresh(new_reserve)
    return new_reserve

@reserve_router.get("/reserve", response_model=List[ReserveResponse],status_code=status.HTTP_200_OK)
def get_reserve(db:Session=Depends(get_db)):
    return db.query(Reserve).all()

@reserve_router.put("/reserve/{id}", response_model=ReserveResponse, status_code=status.HTTP_200_OK)
def update(id:str,reserve_update = ReserveUpdate,db:Session=Depends(get_db)):
    reserve = db.query(Reserve).filter(Reserve.id==id).first()
    if not reserve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    reserve.update(reserve_update)
    db.commit()
    db.refresh(reserve)
    return reserve

@reserve_router.delete("/reserve/{id}",response_model=ReserveResponse, status_code = status.HTTP_200_OK)
def delete(id:str,db:Session=Depends(get_db)):
    reserve = db.query(Reserve).filter(Reserve.id==id).first()
    if not reserve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(reserve)
    db.commit()
    db.refresh(reserve)
    return reserve

