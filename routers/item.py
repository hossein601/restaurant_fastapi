from typing import  Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from dependencies import get_current_user, role_checker
from database.base import get_db
from models.item import Item
from models.user import User
from schemas.item import ItemCreate, ItemResponse, ItemUpdate, ItemInfoResponse, ItemInfo
item_router = APIRouter()

@item_router.post("/item", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_checker(["admin"]))])
def create_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_item = Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

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
    db.delete(item)
    db.commit()
    return {"success": True}


@item_router.get("/item/search", status_code=status.HTTP_200_OK, response_model=ItemInfoResponse,
                 dependencies=[Depends(role_checker(["admin","user"]))])
def search_items(
        name: Optional[str] = Query(None, description="Filter by item name"),
        min_price: Optional[int] = Query(None, description="Minimum Price"),
        max_price: Optional[int] = Query(None, description="Maximum price "),
        get_item_byid :Optional[int]= Query(None, description="Get item by id"),
        in_stock: Optional[bool] = Query(None, description="Stock"),
        get_all_item :Optional[bool]=Query(None, description="Get all item"),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    query = db.query(Item)

    if name:
        query = query.filter(Item.name.ilike(f"%{name}%"))
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    if max_price is not None:
        query = query.filter(Item.price <= max_price)
    if in_stock is not None:
        query = query.filter(Item.stock > 0)
    if get_item_byid is not None:
        query = query.filter(Item.id == get_item_byid)
    if get_all_item is not None:
        query = query

    items = query.all()
    response = [ItemInfo(id = item.id,name=item.name, price=item.price, description=item.description, stock=item.stock) for item in items]
    return ItemInfoResponse(items=response)

@item_router.get("/item/search/min_price", status_code=status.HTTP_200_OK, response_model=ItemInfoResponse,
                 dependencies=[Depends(role_checker(["admin","user"]))])
def search_items_min_price(
        min_price: Optional[int] = Query(None, description="Minimum Price"),
        db: Session = Depends(get_db),
):
    query = db.query(Item)
    if min_price:
        query = query.filter(Item.price >= min_price)
    sorted_items = query.order_by(Item.price).all()
    response = [
        ItemInfo(
            id=item.id,
            name=item.name,
            price=item.price,
            description=item.description,
            stock=item.stock
        )
        for item in sorted_items
    ]

    return ItemInfoResponse(items=response)
