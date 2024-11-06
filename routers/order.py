# routers/order_router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.order import Order
from models.order_item import OrderItem
from models.item import Item
from models.user import User
from schemas.order import OrderCreate, OrderResponse, OrderUpdate
from database.base import get_db

order_router = APIRouter()

@order_router.post("/order", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == order_data.phone_number).first()
    if not user:
        user = User(name=order_data.customer_name, phone_number=order_data.phone_number, wallet=0)
        db.add(user)
        db.commit()
    order = Order(customer_name=order_data.customer_name, phone_number=order_data.phone_number, user=user)
    db.add(order)

    total_price = 0

    for item_data in order_data.items:
        item = db.query(Item).filter(Item.name == item_data.item_name).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if item.stock < item_data.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        order_item = OrderItem(order=order, item=item, quantity=item_data.quantity)
        db.add(order_item)
        item.decrease_stock(item_data.quantity)
        total_price += item.price * item_data.quantity

    order.total_price = total_price
    db.commit()
    return order


@order_router.get("/order", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


@order_router.get("/order/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@order_router.put("/order/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    for item in order.order_items:
        item.item.stock += item.quantity
        db.delete(item)
    db.commit()

    total_price = 0
    for item_data in order_update.items:
        item = db.query(Item).filter(Item.name == item_data.item_name).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if item.stock < item_data.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        order_item = OrderItem(order=order, item=item, quantity=item_data.quantity)
        db.add(order_item)
        item.decrease_stock(item_data.quantity)
        total_price += item.price * item_data.quantity

    order.total_price = total_price
    db.commit()
    return order


@order_router.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    for item in order.order_items:
        item.item.stock += item.quantity
        db.delete(item)
    db.delete(order)
    db.commit()
    return
