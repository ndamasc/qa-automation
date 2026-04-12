import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from api.main import app
from api.db.base import Base
from api.db.session import get_db
from api.services.user_service import hash_password
from config import TEST_DATABASE_URL
from api.db.models.user_model import User

fake = Faker('pt_BR')

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# 🔹 cria tabela UMA vez só
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def create_aleatory_user(client):
    user = {
        "name": fake.first_name(),
        "email": fake.email(),
        "password": "012345678"  # At least 8 chars
    }

    response = client.post("/users/", json=user)
    assert response.status_code == 201  # Created
    return response


@pytest.fixture(scope="function")
def existing_user(db):

    hashed_password = hash_password("password")
    user = User(name="Existing", email="existing@example.com", password=hashed_password)
    db.add(user)
    db.commit()
    return {"name": "Existing", "email": "existing@example.com", "password": "password"}