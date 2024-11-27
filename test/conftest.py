# tests/conftest.py
from datetime import timedelta, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base, get_db
from main import app
from fastapi.testclient import TestClient
import jwt


SECRET_KEY = "17cc637a3dedf881022df527e03936a740f205e1b1991d73ed01e5a40dd0607e"
ALGORITHM = "HS256"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/test_rest8"

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

import bcrypt
from models import Category, Item
from models.user import User

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    hashed_password = bcrypt.hashpw("password".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = User(
        name="hossein",
        phone_number="09014751762",
        wallet=100,
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
    db = TestingSessionLocal()
    hashed_password = bcrypt.hashpw("adminpassword".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    admin = User(
        name="hassan",
        phone_number="09012345678",
        wallet=200,
        role="admin",
        hashed_password=hashed_password,
        address="shargi",
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    yield admin
    db.delete(admin)
    db.commit()

@pytest.fixture
def test_category():
    db = TestingSessionLocal()
    category = Category(
        id =1,
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
    db = TestingSessionLocal()
    item = Item(
        id = 1,
        name="kabab",
        description="Iranian food",
        price=20,
        stock=10,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    yield item
    db.delete(item)