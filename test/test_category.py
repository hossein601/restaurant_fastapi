from models import Category
from test.conftest import generate_test_token, TestingSessionLocal

def test_create_category(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/category/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "vegan", "description": "category"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "vegan"
    assert data["description"] == "category"


def test_update_category(client, test_admin, test_category):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        f"/v1/category/{test_category.id}",
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
        "/v1/category/99/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "new_name", "description": "new_description"},
    )
    assert response.status_code == 404


def test_delete_category(client, test_admin, test_category):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.delete(
        f"/v1/category/{test_category.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204


def test_search_categories_by_name(client, test_admin, test_category):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.get(
        f"/v1/category/search?name={test_category.name}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200



def test_get_all_categories(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.get(
        "/v1/category/search?get_category=true",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
