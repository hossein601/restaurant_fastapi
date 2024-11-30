from models import Basket, BasketItem
from test.conftest import generate_test_token, TestingSessionLocal


def test_create_basket(client, test_user, test_item,test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post(
        "/v1/basket/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": 1, "quantity": 3},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["item_id"] == 1
    assert data["quantity"] == 3

def test_create_basket(client, test_admin, test_item,test_basket_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/basket/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": 1, "quantity": 3},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["item_id"] == test_basket_item.id
    assert data["quantity"] == 3


def test_get_basket(client, test_user, test_basket, test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.get(
        "/v1/basket/",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["items"][0]["item_id"] == test_basket_item.item_id
    assert data["items"][0]["quantity"] == test_basket_item.quantity



def test_update_basket_item(client, test_user,test_basket,test_item, test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.put(
        f"/v1/basket/{test_basket_item.item_id}/10",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    print(response.status_code)
    print(data)
    assert response.status_code == 200
    db = TestingSessionLocal()
    basket_item = db.query(BasketItem).filter(BasketItem.id == test_basket_item.id).first()
    assert basket_item.quantity == 10



def test_delete_basket(client, test_user, test_basket):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.delete(
        "/v1/basket/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    db = TestingSessionLocal()
    basket_item = db.query(BasketItem).filter(BasketItem.id == test_basket_item.id).first()
    assert basket_item is None


def test_delete_basket(client, test_admin, test_basket):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.delete(
        "/v1/basket/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


