from test.conftest import generate_test_token

def test_assign_item_to_category(client,test_item_without_category,test_admin,test_category,test_item):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
            f"/v1/category_item/1/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 201


def test_get_item_for_categories(client,test_category_item,test_admin,test_category,test_item):
    token = generate_test_token(user_id=test_admin.id,role = test_admin.role)
    response = client.get(
        f"/v1/category_item/{test_category.id}",
        headers={"Authorization": f"Bearer {token}"},

    )
    data = response.json()
    assert response.status_code == 200

def test_update_item_categories(client, test_category_item, test_admin, test_category_new):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        f"/v1/category_item/{test_category_item.category_id}/{test_category_item.item_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"category_id": test_category_new.id},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["category_id"] == test_category_new.id
    print(data)

def test_update_item_categories_invalid_id(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        "/v1/category_item/9/9",
        headers={"Authorization": f"Bearer {token}"},
        json={"category_id": 1},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_update_item_categories_unauthorized(client, test_category_item):
    response = client.put(
        f"/v1/category_item/{test_category_item.category_id}/{test_category_item.item_id}",
        json={"category_id": 2},
    )
    assert response.status_code == 403
