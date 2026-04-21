from utils.logger import logger
from faker import Faker

fake = Faker()

def test_create_user(create_user_e2e):   
    
    data = create_user_e2e

    logger.info("1. Test of user creation passed successfully.")
    logger.info(f"User created: {data}") 

    # validação
    assert data.status == 201
    


def test_list_users(api_request):
    
    response = api_request.get("/users/")
    data = response.json()

    assert response.status == 200
    assert isinstance(data, list)
    assert len(data) > 0

    logger.info("2. Users listed successfully")


def test_get_user(api_request, create_user_e2e):

    user = create_user_e2e.json()
    response = api_request.get(f"/users/{user['id']}")
    data = response.json()

    assert response.status == 200
    assert data["id"] == user["id"]
    assert data["name"] == user["name"]
    assert data["email"] == user["email"]

    logger.info("3. User fetched successfully")


def test_update_user(api_request, create_user_e2e):
    user = create_user_e2e.json()

    response = api_request.patch(f"/users/{user['id']}/",data={"email": fake.email()})

    assert response.status == 200
    assert user["name"] == response.json()["name"]
    assert user["email"] != response.json()["email"]


def test_delete_user(api_request, create_user_e2e):

    user = create_user_e2e.json()

    response = api_request.delete(f"/users/{user['id']}")

    assert response.status == 204

    response = api_request.get(f"/users/{user['id']}")
    assert response.status == 404

    logger.info("5. User deleted successfully")


