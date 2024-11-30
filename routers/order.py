from sqlalchemy import event
from models.order import Order
from models.order_item import OrderItem
from models.item import Item
from models.staff import Staff
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import BasketItem
from models.basket import Basket
from database.base import get_db
from dependencies import get_current_user, role_checker
from models.user import User
order_router = APIRouter()


@order_router.post("/order/", status_code=status.HTTP_201_CREATED,dependencies=[Depends(role_checker(["user", "admin"]))])

def create_order(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not user_basket or not user_basket.basket_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Basket is empty")

    order = Order(customer_name=current_user.name,phone_number=current_user.phone_number,user_id=current_user.id,
        address=current_user.address               )
    db.add(order)
    db.commit()
    db.refresh(order)

    total_price = 0
    for basket_item in user_basket.basket_items:
        item = db.query(Item).filter(Item.id == basket_item.item_id).first()
        if not item:
            continue

        if item.stock < basket_item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Not enough stock for {item.name}")

        order_item = OrderItem(
            order_id=order.id,
            item_id=item.id,
            quantity=basket_item.quantity,
        )
        db.add(order_item)
        total_price += item.price * basket_item.quantity
    order.total_price = total_price
    db.commit()

    db.query(BasketItem).filter(BasketItem.basket_id == user_basket.id).delete()
    db.commit()

    return {"order_id": order.id, "total_price": total_price}

def decrease_item_quantity(mapper, connection, target):
    with Session(bind=connection) as db:
        item = db.query(Item).filter(Item.id == target.item_id).one_or_none()
        if item.stock >= target.quantity:
            item.stock -= target.quantity
            db.add(item)

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Not enough stock for {item.name}")

        db.commit()

event.listen(OrderItem, 'after_insert', decrease_item_quantity)







