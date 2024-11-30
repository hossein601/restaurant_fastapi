from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.staff import Staff
from database.base import get_db
from dependencies import role_checker
from schemas.staff import StaffResponse, StaffCreate, StaffUpdate
staff_router = APIRouter()
@staff_router.post("/staff", response_model=StaffResponse, status_code=status.HTTP_201_CREATED,
                   dependencies=[Depends(role_checker(["admin"]))])
def create_staff(staff_data: StaffCreate, db: Session = Depends(get_db)):
    new_staff = Staff(**staff_data.dict())
    db.add(new_staff)
    db.commit()

    db.refresh(new_staff)
    return new_staff


@staff_router.put("/staff/{staff_id}", response_model=StaffResponse, status_code=status.HTTP_200_OK,
                  dependencies=[Depends(role_checker(["admin"]))])
def update_staff(staff_id: int, staff_update: StaffUpdate, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    staff_data = staff_update.dict(exclude_unset=True)
    db.query(Staff).filter(Staff.id == staff_id).update(staff_data)
    db.commit()

    db.refresh(staff)
    return staff



@staff_router.delete("/staff/{staff_id}", status_code=status.HTTP_204_NO_CONTENT,
                     dependencies=[Depends(role_checker(["admin"]))])
def delete_staff(staff_id: int, db: Session = Depends(get_db)):

    staff = db.query(Staff).filter(Staff.id == staff_id).one_or_none()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    db.delete(staff)
    db.commit()

    return {"message": f"Staff member  {staff_id} has been deleted"}
