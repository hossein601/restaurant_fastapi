# routers/order_router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.staff import Staff
from database.base import get_db
from schemas.staff import StaffResponse, StaffCreate, StaffUpdate

staff_router = APIRouter()

@staff_router.post("/staff",response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
def create_staff(staff_data:StaffCreate,db:Session=Depends(get_db)):
    new_staff = Staff(**staff_data.dict())
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return new_staff

@staff_router.get("/staff",response_model=List[StaffResponse], status_code=status.HTTP_200_OK)
def get_staff(db:Session=Depends(get_db)):
    staff = db.query(Staff).all()
    return staff

@staff_router.put("/staff/{phone_number}",response_model=StaffResponse, status_code=status.HTTP_200_OK)
def update_staff(phone_number:str,staff_update:StaffUpdate,db:Session=Depends(get_db)):
    staff = db.query(Staff).filter_by(phone_number=phone_number)
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Staff not found")
    staff.update(staff_update)
    db.commit()
    db.refresh(staff_update)
    return staff_update

@staff_router.delete("/staff/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(phone_number:str,db:Session=Depends(get_db)):
    staff = db.query(Staff).filter_by(phone_number=phone_number).one_or_none()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Staff not found")
    db.delete(staff)
    db.commit()
    db.refresh(staff)
    return staff


