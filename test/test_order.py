from models import Item
from models import basket_item
from test.conftest import generate_test_token, TestingSessionLocal


def test_create_order_basket_empty(client, test_admin,test_basket):
    token = generate_test_token(user_id=test_admin.id, role=test_admin.role)
    response = client.post(
        "/v1/order/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert response.json()["detail"]  == "Basket is empty"

def test_create_order_success(client, test_user, test_basket_item):
    token = generate_test_token(user_id=test_user.id, role=test_user.role)
    response = client.post(
        "/v1/order/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    with TestingSessionLocal() as db:
        item = db.query(Item).filter(Item.id == test_basket_item.item_id).one()
        assert item.stock == 7

