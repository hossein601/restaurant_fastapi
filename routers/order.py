from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.iterables import paginate
from sqlalchemy import event
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from models.order import Order
from models.order_item import OrderItem
from models.item import Item
from models.basket import Basket
from models.basket_item import BasketItem
from database.base import get_db
from dependencies import get_current_user, role_checker
from models.user import User
from schemas.order import  OrderGetResponsePaginate

order_router = APIRouter()

@order_router.post("/orders/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_checker(["user", "admin"]))])
def create_order(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not user_basket or not user_basket.basket_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Create Basket first")
    if current_user.address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enter your address")

    order = Order(
        customer_name=current_user.name,
        phone_number=current_user.phone_number,
        user_id=current_user.id,
        address=current_user.address
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    total_price = 0
    for basket_item in user_basket.basket_items:
        item = db.query(Item).filter(Item.id == basket_item.item_id).first()

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
    if order.total_price == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Create Basket first")
    db.commit()

    db.query(BasketItem).filter(BasketItem.basket_id == user_basket.id).delete()
    db.commit()

    return {"order_id": order.id, "total_price": total_price}

def decrease_item_quantity(mapper, connection, target):
    with Session(bind=connection) as session:
        item = session.query(Item).filter(Item.id == target.item_id).first()
        if not item or item.stock < target.quantity:
            raise Exception(f"Not enough stock for item  {target.item_id}")
        item.stock -= target.quantity
        session.commit()



event.listen(OrderItem, 'after_insert', decrease_item_quantity)
@order_router.get("/orders/", status_code=status.HTTP_200_OK, response_model=LimitOffsetPage[OrderGetResponsePaginate],dependencies=[Depends(role_checker(["user", "admin"]))])
def get_order(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    orders =db.query(Order).join(OrderItem).filter(Order.user_id == current_user.id).all()

    order = []
    for ordering in orders:
        order.append({
            "order_id": ordering.id,
            "customer_name": ordering.customer_name,
            "phone_number": ordering.phone_number,
            "user_id": ordering.user_id,
            "address": ordering.address,
            "total_price": ordering.total_price,
            "items":[{
                "item_id": item.item_id,
                "quantity": item.quantity,
            }for item in ordering.order_items]

        })
    return paginate(order)
























