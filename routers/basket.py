from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import BasketItem
from models.basket import Basket
from database.base import get_db
from schemas.basket import BasketCreateItem, BasketResponse, BasketItemResponse
from dependencies import get_current_user, role_checker
from models.user import User

basket_router = APIRouter()
@basket_router.post("/basket/", status_code=status.HTTP_201_CREATED, response_model=BasketResponse,
                    dependencies=[Depends(role_checker(["user", "admin"]))])
def create_basket(basket_items: BasketCreateItem, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    user_basket = db.query(Basket).filter(Basket.user_id == current_user.id).one_or_none()
    if not user_basket:
        user_basket = Basket(user_id=current_user.id)
        db.add(user_basket)
        db.commit()
        db.refresh(user_basket)

    basket_item = BasketItem(
        quantity=basket_items.quantity,
        item_id=basket_items.item_id,
        basket_id=user_basket.id,
    )
    db.add(basket_item)
    db.commit()
    db.refresh(basket_item)


    return basket_item


@basket_router.get("/basket/", status_code=status.HTTP_200_OK, response_model=BasketItemResponse,
                   dependencies=[Depends(role_checker(["user", "admin"]))])
def get_basket(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    user_basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not user_basket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Basket not found")

    basket_items = db.query(BasketItem).filter(BasketItem.basket_id == user_basket.id).all()
    BasketOutPut = [BasketResponse(item_id=item.item_id, quantity=item.quantity) for item in basket_items]
    return BasketItemResponse(items=BasketOutPut)


@basket_router.put("/basket/{item_id}/{quantity}", status_code=status.HTTP_200_OK, response_model=BasketResponse,
                   dependencies=[Depends(role_checker(["user", "admin"]))])

def update_basket_item(item_id: int,quantity: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    user_basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not user_basket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Basket not found")

    basket_item = (db.query(BasketItem).filter(BasketItem.basket_id == user_basket.id,BasketItem.item_id == item_id).first())

    if not basket_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no item ")

    basket_item.quantity = quantity
    db.commit()
    db.refresh(basket_item)

    return BasketResponse(item_id=basket_item.item_id, quantity=basket_item.quantity)


@basket_router.delete("/basket/", status_code=status.HTTP_200_OK,
                      dependencies=[Depends(role_checker(["user", "admin"]))])
def delete_basket(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):

    user_basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()

    if not user_basket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Basket not found")

    db.query(BasketItem).filter(BasketItem.basket_id == user_basket.id).delete()
    db.commit()

    return {"message": "Basket deleted"}
