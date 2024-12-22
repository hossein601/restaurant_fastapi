from fastapi_pagination import add_pagination

from main import app
from test.conftest import generate_test_token, TestingSessionLocal
from models import Item, BasketItem, Order, OrderItem, User


def test_create_order_basket_empty(client, test_user):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post("v1/orders/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    data =response.json()
    assert data["detail"] == "Create Basket first"

def test_create_order_missing_address(client, test_user, test_basket_item):
    with TestingSessionLocal() as db:
        user = db.query(User).filter(User.id == test_user.id).one()
        user.address = None
        db.commit()

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post("v1/orders/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Enter your address"

def test_create_order(client, test_user, test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post("v1/orders/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201

    with TestingSessionLocal() as db:
        item = db.query(Item).filter(Item.id == test_basket_item.item_id).one()
        assert item.stock == 9

def test_create_order_not_enough__stock(client, test_user, test_basket_item):
    with TestingSessionLocal() as db:
        item = db.query(Item).filter(Item.id == test_basket_item.item_id).one()
        item.stock = 0
        db.commit()
        item_name = item.name

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post("v1/orders/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400

def test_get_orders(client, test_user, test_basket_item):
    add_pagination(app)

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post("v1/orders/", headers={"Authorization": f"Bearer {token}"},params={"limit": 1,"offset":0})
    assert response.status_code == 201

    response = client.get("v1/orders/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


