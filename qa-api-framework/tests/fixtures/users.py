import pytest
from faker import Faker
from api.services.user_service import hash_password
from api.db.models.user_model import User

fake = Faker('pt_BR')



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


@pytest.fixture
def create_user_e2e(api_request):
    response = api_request.post(
        "/users/",
        data={
            "name": fake.first_name(),
            "email": fake.email(),
            "password": "12345678"
        }
    )
    return response

@pytest.fixture(scope="function")
def existing_user(db):

    hashed_password = hash_password("password")
    user = User(name="Existing", email="existing@example.com", password=hashed_password)
    db.add(user)
    db.commit()
    return {"name": "Existing", "email": "existing@example.com", "password": "password"}
