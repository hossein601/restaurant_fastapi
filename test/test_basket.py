from models import Basket, BasketItem
from test.conftest import generate_test_token, TestingSessionLocal


def test_create_basket(client, test_user, test_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post(
        "/v1/basket/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": test_item.id, "quantity": 3},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["item_id"] == test_item.id
    assert data["quantity"] == 3


def test_get_basket(client, test_user, test_basket, test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.get(
        "/v1/basket/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) > 0
    assert data["items"][0]["item_id"] == test_basket_item.item_id
    assert data["items"][0]["quantity"] == test_basket_item.quantity


def test_update_basket_item(client, test_user, test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    updated_quantity = 5
    response = client.put(
        "/v1/basket/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": test_basket_item.item_id, "quantity": updated_quantity},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == test_basket_item.item_id
    assert data["quantity"] == updated_quantity

    db = TestingSessionLocal()
    basket_item = db.query(BasketItem).filter(BasketItem.id == test_basket_item.id).first()
    assert basket_item.quantity == updated_quantity


def test_delete_basket(client, test_user, test_basket):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.delete(
        "/v1/basket/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Basket deleted"

    db = TestingSessionLocal()
    basket_items = db.query(BasketItem).filter(BasketItem.basket_id == test_basket.id).all()
    assert len(basket_items) == 0
