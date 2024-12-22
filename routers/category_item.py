from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.orm import Session
from models import  CategoryItem, Item, Category
from database.base import get_db
from dependencies import get_current_user, role_checker
from models.user import User
from schemas.category_item import CategoryItemResponse, CategoryItemListResponse, \
    CategoryItemUpdate, Category_item_to_category, CategoryItemUpdateOut, Category_assign_item

category_item_router = APIRouter()

@category_item_router.get("/category_items/{category_id}/", status_code=status.HTTP_200_OK, response_model=LimitOffsetPage[CategoryItemResponse] ,
                          dependencies=[Depends(role_checker(["admin","user"]))])
def get_items_for_category(category_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    category_items = db.query(CategoryItem).filter(CategoryItem.category_id == category_id).all()
    items = [db.query(Item).filter(Item.id == per.item_id).first() for per in category_items]
    categoyItemOut = [CategoryItemResponse(id = per.id,name =per.name,price = per.price,stock = per.stock)for per in items]
    return paginate(categoyItemOut)


@category_item_router.post("/category_items/{category_id}/",response_model=Category_item_to_category, status_code=status.HTTP_201_CREATED,
                           dependencies=[Depends(role_checker(["admin"]))])
def assign_item_to_category(category_id: int,data:Category_assign_item,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    item = db.query(Item).filter(Item.id == data.item_id).one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    category_item = db.query(CategoryItem).filter(CategoryItem.category_id == category_id, CategoryItem.item_id == data.item_id).one_or_none()
    if category_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item is assigned to category")

    category_item = CategoryItem(category_id=category_id, item_id=data.item_id)
    db.add(category_item)
    db.commit()
    return category_item

@category_item_router.put("/category_items/{id_category}/", status_code=status.HTTP_201_CREATED,
                          response_model=CategoryItemUpdateOut, dependencies=[Depends(role_checker(["admin"]))])
def update_item_categories(data:CategoryItemUpdate,id_category: int ,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    category_item = db.query(CategoryItem).filter(CategoryItem.category_id == id_category, CategoryItem.item_id == data.item_id).one_or_none()
    if not category_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    category_item.category_id = data.category_id
    db.commit()
    db.refresh(category_item)
    return category_item

@category_item_router.delete("/category_items/", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_item(item_id: int,category_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    category_item = db.query(CategoryItem).filter(CategoryItem.category_id == category_id, CategoryItem.item_id == item_id,).one_or_none()

    if not category_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CategoryItem not found")

    db.delete(category_item)
    db.commit()
    return {"message": "Category_item_deleted"}










