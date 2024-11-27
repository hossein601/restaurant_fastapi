# tests/test_category.py
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
        json={"name": "new_category", "description": "new_description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    db = TestingSessionLocal()
    category = db.query(Category).get(test_category.id)
    assert category.name == "new_category"
    assert category.description == "new_description"

def test_assign_category(client, test_admin, test_category,test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/category/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "vegan", "description": "category"},
    )

