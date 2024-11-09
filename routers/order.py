from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.order import Order
from models.order_item import OrderItem
from models.item import Item
from models.staff import Staff
from schemas.order import OrderCreate, OrderResponse, OrderUpdate
from database.base import get_db
from dependencies import get_current_user, role_checker
from models.user import User

order_router = APIRouter()

def assign_staff(db: Session) -> Staff:

    staff = db.query(Staff).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No staff member available")
    return staff

@order_router.post("/order/create_order",  status_code=status.HTTP_201_CREATED,dependencies=[Depends(role_checker(["user", "admin"]))])
def creat_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    staff = assign_staff(db)

    if not current_user.address:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User should have address.")

    total_price = 0

    for item_data in order_data.items:
        item = db.query(Item).filter(Item.name == item_data.item_name).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item '{item_data.item_name}' not found")
        if item.stock < item_data.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock for '{item_data.item_name}'")

        total_price += item.price * item_data.quantity
    new_order = Order(customer_name=current_user.name,phone_number=current_user.phone_number,total_price=total_price,
                      user_id=current_user.id,staff_id = staff.id, )
    db.add(new_order)
    db.commit()

    db.refresh(new_order)
    return new_order

@order_router.get("/order/get_all_order", response_model=OrderResponse, status_code=status.HTTP_200_OK,
                  dependencies=[Depends(role_checker(["user", "admin"]))])
def get_all_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role == "admin":
        orders = db.query(Order).all()
    else:
        orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders


@order_router.put("/order/{order_id}", status_code=status.HTTP_200_OK,
                  dependencies=[Depends(role_checker(["admin"]))])
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    for order_item in order.order_items:
        order_item.item.stock += order_item.quantity
        db.delete(order_item)
    db.commit()

    assigned_staff = assign_staff(db)
    order.staff = assigned_staff

    total_price = 0
    for item_data in order_update.items:
        item = db.query(Item).filter(Item.name == item_data.item_name).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item '{item_data.item_name}' not found")
        if item.stock < item_data.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"not enough stock for '{item_data.item_name}'")

        order_item = OrderItem(order=order, item=item, quantity=item_data.quantity)
        db.add(order_item)
        item.stock -= item_data.quantity
        total_price += item.price * item_data.quantity

    order.total_price = total_price
    db.commit()

    db.refresh(order)

    return {"massage":"created"}


@order_router.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT,
                     dependencies=[Depends(role_checker(["admin"]))])
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    order = db.query(Order).filter(Order.id == order_id).one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    for order_item in order.order_items:
        order_item.item.stock += order_item.quantity
        db.delete(order_item)

    db.delete(order)
    db.commit()

    return {"message": "Order deleted."}
