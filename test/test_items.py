from models import Item
from test.conftest import generate_test_token, TestingSessionLocal


def test_create_item(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/item",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "gheime",
            "description": "food",
            "price": 30,
            "stock": 15,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "gheime"
    assert data["description"] == "food"
    assert data["price"] == 30
    assert data["stock"] == 15

def test_update_item(client, test_admin, test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        f"/v1/item/{test_item.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "ghorme", "description": "food", "price": 20, "stock": 10},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ghorme"
    assert data["description"] == "food"

def test_update_item_not_exsist(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        "/v1/item/99",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "ghorme", "description": "food", "price": 20, "stock": 10},
    )
    assert response.status_code == 404


def test_delete_item(client,test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.delete(
        "/v1/item/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204


def test_search_item(client, test_admin, test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.get(
        "/v1/item/search",
        headers={"Authorization": f"Bearer {token}"},
        params={"name": "kabab"}
    )
    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    item = data["items"][0]
    assert item["name"] == "kabab"
    assert item["description"] == "Iranian food"
    assert item["price"] == 20
    assert item["stock"] == 10


def test_search_item_min_price(client, test_admin, test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.get(
        "/v1/item/search/min_price",
        headers={"Authorization": f"Bearer {token}"},
        params={"min_price": 10},
    )
    assert response.status_code == 200




