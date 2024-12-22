from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.orm import Session
from typing import Optional
from database.base import get_db
from models.category import Category
from schemas.category import CategoryCreate, CategoryResponse, CategoryInfoResponse, CategoryInfo
from dependencies import get_current_user, role_checker
from models.user import User

category_router = APIRouter()


@category_router.post("/categories/", status_code=status.HTTP_201_CREATED, response_model=CategoryInfo,
                      dependencies=[Depends(role_checker(["admin"]))])
def create_category(data: CategoryCreate, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    category = db.query(Category).filter(Category.name == data.name).first()
    if category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    category = Category(name=data.name, description=data.description)
    db.add(category)
    db.commit()

    db.refresh(category)
    return category


@category_router.put("/categories/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse,
                     dependencies=[Depends(role_checker(["admin"]))])
def update_category(category_id: str, data: CategoryCreate, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    category.name = data.name
    category.description = data.description
    db.commit()
    db.refresh(category)
    return CategoryResponse(
        message=f"Category updated with name {category.name} and description {category.description}")


@category_router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT,
                        dependencies=[Depends(role_checker(["admin"]))])
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}


@category_router.get("/categories/", status_code=status.HTTP_200_OK, response_model=LimitOffsetPage[CategoryInfo],
                     dependencies=[Depends(role_checker(["admin","user"]))])
def search_categories(name: Optional[str] = Query(None, description="Filter by category name"),
                      description: Optional[str] = Query(None, description="Filter by category description"),
                      get_category :Optional[bool] =Query(None, description="Get all categories"),
                      db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):

    query = db.query(Category)
    if name:
        query = query.filter(Category.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Category.description.ilike(f"%{description}%"))
    if get_category:
        query= query
    categories = query.all()
    response = [CategoryInfo(id = category.id,name=category.name, description=category.description, created_at=category.created_time) for category in
                categories]
    return paginate(response)