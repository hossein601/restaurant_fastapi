from test.conftest import generate_test_token, test_category_item, TestingSessionLocal
from fastapi_pagination import add_pagination
from main import app

def test_assign_item_to_category(client,test_item_without_category,test_admin,test_category,test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
            f"/v1/category_items/1/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id":1}
    )
    data = response.json()
    assert response.status_code == 201

def test_assign_item_to_category_not_found_item(client,test_item_without_category,test_admin,test_category,test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
            f"/v1/category_items/{test_category.id}/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id":50}
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Item not found"


def test_assign_item_to_category_exist_category_item(client,test_item_without_category,test_category_item,test_admin,test_category,test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        f"/v1/category_items/{test_category_item.category_id}/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": test_category_item.item_id}
    )
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "Item is assigned to category"



def test_assign_item_to_category_not_found_cateory(client,test_item_without_category,test_admin,test_category,test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
            f"/v1/category_items/50/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id":1}
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Category not found"



def test_update_item_categories_not_exist_item(client, test_category_item, test_admin, test_category_new,test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        f"/v1/category_items/{test_category_item.category_id}/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": test_item.id,"category_id": test_category_item.category_id},
    )
    assert response.status_code == 201
    data = response.json()



def test_update_item_categories_not_found_item(client, test_category_item, test_admin, test_category_new,test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        f"/v1/category_items/{test_category_item.category_id}/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id": 20,"category_id": test_category_item.category_id},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"]=="Item not found"


def test_update_item_categories_not_found_category(client, test_category_item, test_admin, test_category_new,test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        f"/v1/category_items/99/",
        headers={"Authorization": f"Bearer {token}"},
        json={"item_id":test_category_item.item_id, "category_id": test_category_item.category_id},
    )
    assert response.status_code == 404



def test_update_item_categories_invalid_id(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        "/v1/category_item/9/9",
        headers={"Authorization": f"Bearer {token}"},
        json={"category_id": 1},
    )
    assert response.status_code == 404

def test_get_category_items(client,test_user,test_category_item):
    add_pagination(app)

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.get(
        f"/v1/category_items/{test_category_item.category_id}/",
        headers={"Authorization": f"Bearer {token}"},
        params={"limit":10,"offset":0},
    )
    assert response.status_code == 200

def test_get_category_items__not_exist_category_items(client,test_user,test_category_item):
    add_pagination(app)

    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.get(
        f"/v1/category_items/100/",
        headers={"Authorization": f"Bearer {token}"},
        params={"limit":10,"offset":0},
    )
    assert response.status_code == 404


def test_delete_category_items(client, test_admin, test_category_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.delete(
        "/v1/category_items/",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "item_id": test_category_item.item_id,
            "category_id": test_category_item.category_id,
        },
    )
    assert response.status_code == 204



