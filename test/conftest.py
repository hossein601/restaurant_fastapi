from datetime import timedelta, datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base, get_db
from main import app
from fastapi.testclient import TestClient
import jwt
import bcrypt
from models import Category, Item, Basket, BasketItem, Staff, CategoryItem, Order
from models.user import User

SECRET_KEY = "17cc637a3dedf881022df527e03936a740f205e1b1991d73ed01e5a40dd0607e"
ALGORITHM = "HS256"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/test13"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def generate_test_token(user_id: int, role: str, expires_delta: timedelta = timedelta(hours=1)):
    expire = datetime.utcnow() + expires_delta
    payload = {"sub": str(user_id), "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    with TestingSessionLocal() as db:
        hashed_password = bcrypt.hashpw("1234qwer".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(
            name="hossein",
            phone_number="09014751762",
            wallet=300,
            role="user",
            hashed_password=hashed_password,
            address="arafati",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        yield user
        db.delete(user)
        db.commit()

@pytest.fixture
def test_admin():
    with TestingSessionLocal() as db:
        hashed_password = bcrypt.hashpw("adminpassword".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        admin = User(
            name="hassan",
            phone_number="09012345678",
            wallet=200,
            role="admin",
            hashed_password=hashed_password,
            address="shargi",
            created_time = '2020-12-04T16:26:14.585Z'
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        yield admin
        db.delete(admin)
        db.commit()

@pytest.fixture
def test_category():
    with TestingSessionLocal() as db:
        category = Category(
            name="vegtable",
            description="food",
        )
        db.add(category)
        db.commit()
        db.refresh(category)
        yield category
        db.delete(category)
        db.commit()

@pytest.fixture
def test_item():
    with TestingSessionLocal() as db:
        item = Item(
            name="kabab",
            description="Iranian food",
            price=20,
            stock=10,
            created_time='2020-12-04T16:26:14.585Z',
            max_amount= 20
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        yield item
        db.delete(item)
        db.commit()

@pytest.fixture
def test_item_stock_zero():
    with TestingSessionLocal() as db:
        item = Item(
            name="gheime",
            description="Italian food",
            price=30,
            stock=0,
            created_time='2020-12-04T16:26:14.585Z',
            max_amount= 20
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        yield item
        db.delete(item)
        db.commit()

@pytest.fixture
def test_category_new():
    with TestingSessionLocal() as db:
        category = Category(
            name="vanila",
            description="food",
        )
        db.add(category)
        db.commit()
        db.refresh(category)
        yield category
        db.delete(category)
        db.commit()

@pytest.fixture
def test_category_item(test_item, test_category):
    with TestingSessionLocal() as db:
        category_item = CategoryItem(
            item_id=test_item.id,
            category_id=test_category.id,
        )
        db.add(category_item)
        db.commit()
        db.refresh(category_item)
        yield category_item
        db.delete(category_item)
        db.commit()

@pytest.fixture
def test_basket(test_user):
    with TestingSessionLocal() as db:
        basket = Basket(user_id=test_user.id,)
        db.add(basket)
        db.commit()
        db.refresh(basket)
        yield basket
        db.delete(basket)
        db.commit()


@pytest.fixture
def test_basket_item(test_basket, test_item,test_user):
    with TestingSessionLocal() as db:
        basket_item = BasketItem(
            basket_id=test_basket.id,
            item_id=test_item.id,
            quantity=1,
        )
        db.add(basket_item)
        db.commit()
        db.refresh(basket_item)
        yield basket_item
        db.delete(basket_item)
        db.commit()

@pytest.fixture
def test_basket_not_enough_stock(test_user):
    with TestingSessionLocal() as db:
        basket = Basket(user_id=3,)
        db.add(basket)
        db.commit()
        db.refresh(basket)
        yield basket
        db.delete(basket)
        db.commit()




@pytest.fixture
def test_item_not_enough_stock():
    with TestingSessionLocal() as db:
        item = Item(
            name="kabab",
            description="Iranian food",
            price=20,
            stock=0,
            created_time='2020-12-04T16:26:14.585Z',
            max_amount= 20
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        yield item
        db.delete(item)
        db.commit()


@pytest.fixture
def test_basket_item_not_enough_stock(test_basket, test_item,test_user):
    with TestingSessionLocal() as db:
        basket_item = BasketItem(
            basket_id=test_basket.id,
            item_id=test_item_not_enough_stock.id,
            quantity=1,
        )
        db.add(basket_item)
        db.commit()
        db.refresh(basket_item)
        yield basket_item
        db.delete(basket_item)
        db.commit()


@pytest.fixture
def test_staff():
    with TestingSessionLocal() as db:
        staff = Staff(
            phone_number="09014751765",
            name = "hassan",
            position="chef",
            created_time = '2020-12-04T16:26:14.585Z',
            updated_time = '2021-12-04T16:26:14.585Z',

        )
        db.add(staff)
        db.commit()
        db.refresh(staff)
        yield staff
        db.delete(staff)
        db.commit()

@pytest.fixture
def test_item_without_category():
    with TestingSessionLocal() as db:
        item = Item(
            name="chicken",
            description="Iranian food",
            price=13,
            stock=50,
            max_amount=20
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        yield item
        db.delete(item)

        db.commit()
