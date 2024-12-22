from models import Basket, BasketItem
from test.conftest import generate_test_token, TestingSessionLocal, test_user, test_basket_item
from fastapi_pagination import add_pagination
from main import app


def test_create_basket(client, test_user, test_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": test_item.id, "add": True},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["item_id"] == test_item.id
    assert data["quantity"] == 1

def test_create_basket_basket_item_exist(client, test_user, test_item,test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": test_basket_item.item_id, "add": True},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 1


def test_create_basket_not_exist_basket(client, test_user, test_item_stock_zero, ):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": test_item_stock_zero.id, "add": True},
    )
    assert response.status_code == 406

def test_create_basket_not_item(client, test_user, test_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": 100, "add": True},
    )
    assert response.status_code == 404



def test_add_basket(client, test_user, test_item,test_basket,test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.put(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": test_item.id, "add": True},
    )
    assert response.status_code == 201

def test_add_basket_not_exist_basket(client, test_admin, test_item,test_basket,test_basket_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": test_item.id, "add": True},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"]=="Basket not found for user"


def test_remove_from_basket(client, test_user, test_basket, test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.put(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": test_basket_item.item_id, "add": False},
    )
    assert response.status_code == 200

def test_remove_from_basket_not_exist_bakset(client, test_admin, test_basket, test_basket_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": test_basket_item.item_id, "add": False},
    )
    assert response.status_code == 404

def test_remove_from_basket_not_exist_item(client, test_user, test_basket, test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.put(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": 100, "add": False},
    )
    assert response.status_code == 404

def test_remove_from_basket_not_exist_item(client, test_user, test_basket, test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.put(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": 100, "add": False},
    )
    assert response.status_code == 404


def test_get_basket(client, test_user, test_basket, test_basket_item):
    add_pagination(app)

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.get(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        params={"limit": 10, "offset": 0},
    )
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert len(data["items"]) > 0
    assert data["items"][0]["item_id"] == test_basket_item.item_id
    assert data["items"][0]["quantity"] == test_basket_item.quantity


def test_delete_item_from_basket(client, test_user, test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.delete(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        params={"delete": True, "item_id": test_basket_item.item_id},
    )
    assert response.status_code == 200
    data = response.json()

def test_delete_item_from_basket_not_basket_item(client, test_admin, test_basket_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.delete(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        params={"delete": True, "item_id": test_basket_item.item_id},
    )
    assert response.status_code == 404
    data = response.json()


def test_delete_all_items_from_basket(client, test_user, test_basket):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.delete(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        params={"delete": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Basket deleted"

    db = TestingSessionLocal()
    basket_items = db.query(BasketItem).filter(BasketItem.basket_id == test_basket.id).all()
    assert len(basket_items) == 0


def test_delete_basket_not_found(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.delete(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        params={"delete": True},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Basket not found"


def test_item_not_found_in_basket(client, test_user):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)

    response = client.post(
        "/v1/baskets/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": 9, "add": True},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Item not found"

