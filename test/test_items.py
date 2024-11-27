from test.conftest import generate_test_token


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

def test_update_item(client,test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        "/v1/item",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "ghorme", "description": "food", "price": 20, "stock": 10},
    )
