from models import Staff
from test.conftest import generate_test_token, TestingSessionLocal


def test_create_staff(client,test_admin):
    token = generate_test_token(user_id=test_admin.id,role =test_admin.role)
    response = client.post(
        'v1/staff/',
        headers={'Authorization': f'Bearer {token}'},
        json = {"phone_number":"09354361729","name":"omid","position":"chef"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["phone_number"] == "09354361729"
    assert data["name"] == "omid"

def test_update_staff(client,test_admin,test_staff):
    token = generate_test_token(user_id=test_admin.id,role =test_admin.role)
    response = client.put(
        f'v1/staff/{test_staff.id}',
        headers={'Authorization': f'Bearer {token}'},
        json = {"name":"updated_name","position":"updated_position"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "updated_name"
    assert data["position"] == "updated_position"

def test_update_not_exsisting_staff(client,test_admin):
    token = generate_test_token(user_id=test_admin.id,role =test_admin.role)
    response = client.put(
        'v1/staff/99',
        headers={'Authorization': f'Bearer {token}'},
        json = {"name":"updated_name","position":"updated_position"},
    )
    assert response.status_code == 404


def test_delete_staff(client,test_admin,test_staff):
    token = generate_test_token(user_id=test_admin.id,role =test_admin.role)
    response = client.delete(
        f'v1/staff/{test_staff.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 204

def test_delete_staff_statuscode404(client,test_admin,test_item):
    token = generate_test_token(user_id=test_admin.id,role =test_admin.role)
    response = client.delete(
        f'v1/staff/4',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 404



