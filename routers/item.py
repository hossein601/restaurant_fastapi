
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_filter import FilterDepends
from fastapi_pagination import paginate
from sqlalchemy.orm import Session

from dependencies import get_current_user, role_checker
from database.base import get_db
from models import Category, CategoryItem
from models.item import Item
from models.user import User
from schemas.filter import ItemFilter, FilterResponse
from schemas.item import ItemCreate, ItemResponse, ItemUpdate
from fastapi_pagination.limit_offset import  LimitOffsetPage
from sqlalchemy import select

item_router = APIRouter()

@item_router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_checker(["admin"]))])
def create_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_item = Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

@item_router.put("/items/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(role_checker(["admin"]))])
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data_dict = item_data.dict(exclude_unset=True)
    for key in item_data_dict:
        setattr(item, key, item_data_dict[key])
    db.flush()
    return item

@item_router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_checker(["admin"]))])
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(item)
    db.commit()
    return {"success": True}

@item_router.get("/items",status_code = status.HTTP_200_OK,response_model=LimitOffsetPage[FilterResponse], dependencies=[Depends(role_checker(["admin","user"]))])
def filter_items(item_filter: ItemFilter = FilterDepends(ItemFilter),
                 category_id: int = None,
                 category_name : str = None,
                 db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):

    if item_filter.id or item_filter.price or item_filter.description :
        query = item_filter.filter(select(Item).join(CategoryItem).join(Category)).filter(Item.stock>0)

    if category_id is not None:
        query =db.query(Item).join(CategoryItem).join(Category).filter(Category.id == category_id).filter(Item.stock>0)
    if category_name is not None:
        query = db.query(Item).join(CategoryItem).join(Category).filter(Category.name.ilike(f"%{category_name}%")).filter(Item.stock>0)
    elif not category_id and not category_name and not item_filter.id and not item_filter.price and not item_filter.description:
        query = db.query(Item).join(CategoryItem).join(Category).filter(Item.stock>0)



    result = db.execute(query).scalars().all()
    return paginate(result)


