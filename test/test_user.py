from models import User
from test.conftest import generate_test_token, TestingSessionLocal


def test_get_users_profile(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.get("/v1/users/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "hassan"
    assert data["phone_number"] == "09012345678"
    assert data["wallet"] == 200
    assert data["address"] == "shargi"

def test_increase_wallet(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        "/v1/users/increase_wallet",
        json={"wallet": 50},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["wallet"] == test_admin.wallet + 50

def test_decrease_wallet(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        "/v1/users/decrease_wallet",
        json={"wallet": 50},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["wallet"] == test_admin.wallet - 50

def test_decrease_wallet_get_error(client,test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put(
        "/v1/users/decrease_wallet",
        json={"wallet": 500},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403

