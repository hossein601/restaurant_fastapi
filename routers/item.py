
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.item import Item
from schemas.item import ItemCreate, ItemResponse, ItemUpdate
from database.base import get_db

item_router = APIRouter()


@item_router.post("/create_item", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    new_item = Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@item_router.get("/item", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items


@item_router.put("/item/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    for field, value in item_data.dict(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@item_router.delete("/item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.delete(item)
    db.commit()
    return
