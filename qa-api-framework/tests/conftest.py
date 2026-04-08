import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from api.main import app
from api.db.base import Base
from api.db.session import get_db
from config import TEST_DATABASE_URL # banco de teste

fake = Faker('pt_BR')

engine = create_engine(TEST_DATABASE_URL,connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()

    Base.metadata.create_all(bind=connection)  # 🔥 FALTAVA ISSO

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()

    

@pytest.fixture(scope="function")
def create_aleatory_user(client):
    user = {
        "name": fake.first_name(),
        "email": fake.email(),
        "password": "012345"
        }
    
    response = client.post("/users/", json=user)
    return response
