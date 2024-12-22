from test.conftest import generate_test_token


def test_get_users_profile(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.get("/v1/users/",
                          headers={"Authorization": f"Bearer {token}"})
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

def test_signin_with_valid_data(client):
    response = client.post(
        "/v1/signin",
        json={"phone_number": "09254361631", "password": "Sharfod1234"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

def test_login_with_valid_data(client,test_user):
    response = client.post(
        "/v1/login",
        json={"phone_number": test_user.phone_number, "password": "1234qwer"}
    )
    assert response.status_code == 200
    data = response.json()


def test_login_with_invalid_data(client,test_user):
    response = client.post(
        "/v1/login",
        json={"phone_number": "09374281746", "password": "1234qwer"}
    )
    assert response.status_code == 401


def test_signin_existing_phone_number(client, test_user):
    response = client.post(
        "/v1/signin",
        json={"phone_number": test_user.phone_number, "password": "1234qweQ"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Phone Number already exists"

def test_signin_with_invalid_password(client):
    response = client.post(
        "/v1/signin",
        json={"phone_number": "0987654321", "password": "there"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Password in not valid"

def test_signin_with_invalid_phone_number(client):
    response = client.post(
        "/v1/signin",
        json={"phone_number": "09123", "password": "1234qwer"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Phone number is not valid"

def test_login_with_invalid_phone_number(client):
    response = client.post(
        "/v1/login",
        json={"phone_number": "09123", "password": "1234qwer"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Phone number is not valid"

def test_update_user_profile(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.put("/v1/users/",
                          headers={"Authorization": f"Bearer {token}"},
                          json={"name": "hassan", "address": "asdfjkwkndskfnalk"}
                          )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "hassan"
    assert data["address"] == "asdfjkwkndskfnalk"

def test_delete_user(client, test_admin):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.delete("/v1/users/",
                             headers={"Authorization": f"Bearer {token}"},)

    assert response.status_code == 204

def test_validation_name(client,test_user):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.put(
        "/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "asdfasdddddddddddddddddddddddddddddddddddddddddddddddddddddddddasdddddddddddddddddd","address":"tehran"}
    )
    assert response.status_code == 422
    data = response.json()

def test_validation_address(client,test_user):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.put(
        "/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "hossein","address":"tehranaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasddddddddddddddddddddddddddddddddddddasddddddd"}
    )
    assert response.status_code == 422
    data = response.json()

