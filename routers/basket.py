
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import paginate
from sqlalchemy.orm import Session
from models import BasketItem, Item, GuestUser
from models.basket import Basket
from database.base import get_db
from schemas.basket import BasketCreateItem, BasketResponse, BasketItemResponse
from fastapi_pagination.limit_offset import  LimitOffsetPage
from fastapi import status,Header
basket_router = APIRouter()


@basket_router.post("/baskets/", status_code=status.HTTP_201_CREATED, response_model=BasketResponse)
def create_basket(actions: BasketCreateItem,guest_user_id: int= Header(), db: Session = Depends(get_db)):
    guest_user = db.query(GuestUser).filter(GuestUser.id == guest_user_id).one_or_none()
    if not guest_user:
        guest_user = GuestUser(id = guest_user_id)
        db.add(guest_user)
        db.flush()
    item = db.query(Item).filter(Item.id == actions.item_id).one_or_none()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    guest_user_basket = db.query(Basket).filter(Basket.guest_user_id == guest_user_id).one_or_none()
    if not guest_user_basket:
        guest_user_basket = Basket(guest_user_id=guest_user_id)
        db.add(guest_user_basket)
        db.commit()
        db.refresh(guest_user_basket)

    basket_item = db.query(BasketItem).filter(
        BasketItem.basket_id == guest_user_basket.id, BasketItem.item_id == actions.item_id
    ).one_or_none()

    if basket_item:
        if item.stock > 0 and item.max_amount > 0:
            basket_item.quantity = 1
            db.commit()
            db.refresh(basket_item)
            return basket_item

    if  item.stock > 0 and item.max_amount > 0:
        basket_item = BasketItem(
            quantity=1,
            basket_id=guest_user_basket.id,
            item_id=actions.item_id,
        )
        db.add(basket_item)
        db.commit()
        db.refresh(basket_item)
        return basket_item

    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Item not available ")

@basket_router.put("/baskets/", status_code=status.HTTP_201_CREATED, response_model=BasketResponse)
def add_remove_item(actions: BasketCreateItem,guest_user_id: int= Header(), db: Session = Depends(get_db)):
    guest_user_basket = db.query(Basket).filter(Basket.guest_user_id == guest_user_id).one_or_none()

    if not guest_user_basket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Basket not found for user")

    item = db.query(Item).filter(Item.id == actions.item_id).one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    basket_item = db.query(BasketItem).filter(
        BasketItem.basket_id == guest_user_basket.id, BasketItem.item_id == actions.item_id
    ).one_or_none()
    if not basket_item:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    if  not actions.add:
        if basket_item.quantity > 1:
            basket_item.quantity -= 1
            db.commit()
            db.refresh(basket_item)
            return basket_item

        else:
            basket_item.quantity =0
            db.commit()
            db.refresh(basket_item)
            return {"item_id": actions.item_id,"quantity": 0}

    if  actions.add :
        if item.stock > basket_item.quantity and item.max_amount > basket_item.quantity:
            basket_item.quantity += 1
            db.commit()
            db.refresh(basket_item)
            return basket_item
        
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ّItem is more than max_amount")
@basket_router.get("/baskets/", status_code=status.HTTP_200_OK, response_model=LimitOffsetPage[BasketResponse])
def get_basket(db: Session = Depends(get_db), guest_user_id: int= Header()):

    guest_user_basket = db.query(Basket).filter(Basket.guest_user_id == guest_user_id).one_or_none()

    if not guest_user_basket:
        return BasketItemResponse(items=[])

    basket_items = db.query(BasketItem).filter(BasketItem.basket_id == guest_user_basket.id).all()

    BasketOutPut = [BasketResponse(item_id=item.item_id, quantity=item.quantity) for item in basket_items if item.quantity > 0]

    return paginate(BasketOutPut)

@basket_router.delete("/baskets/", status_code=status.HTTP_200_OK)
def delete_from_basket(delete:bool = None,item_id: int = None , db: Session = Depends(get_db),guest_user_id: int= Header()):
    guest_user_basket = db.query(Basket).filter(Basket.guest_user_id == guest_user_id).one_or_none()

    if not guest_user_basket:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Basket not found")

    if item_id is not None and delete:
        basket_item = db.query(BasketItem).filter(
            BasketItem.basket_id == guest_user_basket.id,
            BasketItem.item_id == item_id
        ).one_or_none()

        db.query(BasketItem).filter(BasketItem.basket_id == guest_user_basket.id,BasketItem.item_id == item_id).delete()
        db.commit()
        return {"message": " Item removed from basket"}

    elif delete:
        db.query(BasketItem).filter(BasketItem.basket_id == guest_user_basket.id).delete()
        db.commit()
        return {"message": "Basket deleted"}

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")



