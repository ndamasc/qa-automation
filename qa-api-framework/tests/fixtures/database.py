import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.main import app
from api.db.base import Base
from api.db.session import get_db

from config import TEST_DATABASE_URL


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