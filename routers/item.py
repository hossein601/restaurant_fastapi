# routers/item_router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_current_user, role_checker
from database.base import get_db
from models.item import Item
from models.user import User
from schemas.item import ItemCreate, ItemResponse, ItemUpdate

item_router = APIRouter()

@item_router.post("/create_item", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_checker(["admin"]))])
def create_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_item = Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

@item_router.get("/items", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
def get_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = db.query(Item).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items

@item_router.put("/item/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(role_checker(["admin"]))])
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item_data_dict = item_data.dict(exclude_unset=True)
    for key in item_data_dict:
        setattr(item, key, item_data_dict[key])

    db.commit()

    return item


@item_router.delete("/item/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_checker(["admin"]))])
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.delete(item)

    db.commit()

    return {"success": True}
