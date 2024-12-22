from test.conftest import generate_test_token
from fastapi_pagination import add_pagination
from main import app


def test_create_item(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "gheime",
            "description": "food",
            "price": 30,
            "stock": 15,
            "created_time ":"2020-12-04T16:26:14.585Z",
            "max_amount": 100,
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
        f"/v1/items/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "ghorme", "description": "food", "price": 20, "stock": 10,"max_amount":20},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ghorme"
    assert data["description"] == "food"

def test_update_item_not_exsist(client, test_admin,test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        "/v1/items/99",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "ghorme", "description": "food", "price": 20, "stock": 10,"max_amount":20},
    )
    assert response.status_code == 404


def test_delete_item(client,test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.delete(
        "/v1/items/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204


def test_filter_item_id(client,test_user,test_item):
    add_pagination(app)

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.get(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        params={"id":test_item.id,"limit":10,"offset":0},
    )
    assert response.status_code == 200

def test_filter_item_price(client,test_user,test_item):
    add_pagination(app)

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.get(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        params={"price":test_item.price,"limit":10,"offset":0},
    )
    assert response.status_code == 200

def test_filter_item_description(client,test_user,test_item):
    add_pagination(app)

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.get(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        params={"description":test_item.description,"limit":10,"offset":0},
    )
    assert response.status_code == 200

def test_filter_item_category_id(client,test_user,test_category_item):
    add_pagination(app)

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.get(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        params={"category_id":test_category_item.category_id,"limit":10,"offset":0},
    )
    assert response.status_code == 200

def test_filter_item_category_name(client,test_user,test_category_item,test_category):
    add_pagination(app)

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.get(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        params={"category_name":test_category.name,"limit":10,"offset":0},
    )
    assert response.status_code == 200
def test_filter_item_category_no_filter(client,test_user,test_category_item,test_category):
    add_pagination(app)

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.get(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        params={"limit":10,"offset":0},
    )
    assert response.status_code == 200


def test_create_item_invalid_name(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "gheimeasdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
            "description": "food",
            "price": 30,
            "stock": 15,
            "created_time ":"2020-12-04T16:26:14.585Z",
            "max_amount": 100,
        },
    )
    assert response.status_code == 422


def test_create_item_invalid_descriptipn(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "ghorme",
            "description": "foodqadsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss",
            "price": 30,
            "stock": 15,
            "created_time ":"2020-12-04T16:26:14.585Z",
            "max_amount": 100,
        },
    )
    assert response.status_code == 422

def test_create_item_invalid_price(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "ghorme",
            "description": "iranian food",
            "price": 301233333333,
            "stock": 15,
            "created_time ":"2020-12-04T16:26:14.585Z",
            "max_amount": 100,
        },
    )
    assert response.status_code == 422

def test_create_item_invalid_stock(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "ghorme",
            "description": "iranian food",
            "price": 30,
            "stock": 15555555555,
            "created_time ":"2020-12-04T16:26:14.585Z",
            "max_amount": 100,
        },
    )
    assert response.status_code == 422
def test_create_item_invalid_max_amount(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "ghorme",
            "description": "iranian food",
            "price": 30,
            "stock": 1234,
            "created_time ":"2020-12-04T16:26:14.585Z",
            "max_amount": 123123123,
        },
    )
    assert response.status_code == 422







