from models import Staff
from test.conftest import generate_test_token, TestingSessionLocal


def test_create_staff(client,test_admin):
    token = generate_test_token(user_id=test_admin.id,role =test_admin.role)
    response = client.post(
        'v1/staffs/',
        headers={'Authorization': f'Bearer {token}'},
        json = {"phone_number":"09354361729","name":"omid","position":"chef","created_time" :"2020-12-04T16:26:14.585Z"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["phone_number"] == "09354361729"
    assert data["name"] == "omid"

def test_update_staff(client,test_admin,test_staff):
    token = generate_test_token(user_id=test_admin.id,role =test_admin.role)
    response = client.put(
        f'v1/staffs/{test_staff.id}',
        headers={'Authorization': f'Bearer {token}'},
        json = {"name":"updated_name","position":"updated_position","updated_time" :"2020-12-04T16:26:14.585Z"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "updated_name"
    assert data["position"] == "updated_position"

def test_update_not_exsisting_staff(client,test_admin):
    token = generate_test_token(user_id=test_admin.id,role =test_admin.role)
    response = client.put(
        'v1/staffs/99',
        headers={'Authorization': f'Bearer {token}'},
        json = {"name":"updated_name","position":"updated_position","updated_time" :"2020-12-04T16:26:14.585Z"},
    )
    assert response.status_code == 404


def test_delete_staff(client,test_admin,test_staff):
    token = generate_test_token(user_id=test_admin.id,role =test_admin.role)
    response = client.delete(
        f'v1/staffs/{test_staff.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 204

def test_delete_staff_not_staff(client,test_admin,test_item):
    token = generate_test_token(user_id=test_admin.id,role =test_admin.role)
    response = client.delete(
        f'v1/staffs/4',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 404



