
from models import Category
from test.conftest import generate_test_token, TestingSessionLocal
from fastapi_pagination import add_pagination
from main import app

def test_create_category(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/categories/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "vegan", "description": "category",},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "vegan"
    assert data["description"] == "category"


def test_create_category_exist(client,test_admin,test_category):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/categories/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": test_category.name, "description": "category",},
    )
    assert response.status_code == 400


def test_update_category(client, test_admin, test_category):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        f"/v1/categories/{test_category.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "new_name", "description": "new_description"},
    )
    assert response.status_code == 200
    data = response.json()
    db = TestingSessionLocal()
    category = db.query(Category).get(test_category.id)
    assert category.name == "new_name"
    assert category.description == "new_description"

def test_update_category_not_exsiting(client, test_admin,):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        "/v1/categories/99/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "new_name", "description": "new_description"},
    )
    assert response.status_code == 404


def test_delete_category(client, test_admin, test_category):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.delete(
        f"/v1/categories/{test_category.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204

def test_delete_category_not_exist(client, test_admin, test_category):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.delete(
        f"/v1/categories/100",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_search_categories_by_name(client, test_admin, test_category):
    add_pagination(app)
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.get(
        f"/v1/categories/",
        headers={"Authorization": f"Bearer {token}"},
        params={"name": test_category.name,"limit": 10, "offset": 0},
    )
    assert response.status_code == 200


def test_search_categories_descriptions(client, test_admin, test_category):
    add_pagination(app)
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.get(
        f"/v1/categories/",
        headers={"Authorization": f"Bearer {token}"},
        params={"description": test_category.description,"limit": 10,"offset": 0},
    )
    assert response.status_code == 200

def test_search_categories_get_all(client, test_admin, test_category):
    add_pagination(app)
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.get(
        f"/v1/categories/",
        headers={"Authorization": f"Bearer {token}"},
        params={"get_category":True,"limit": 10,"offset": 0},
    )
    assert response.status_code == 200



