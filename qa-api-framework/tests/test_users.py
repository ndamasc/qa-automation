from utils.logger import logger

def test_create_user(client, create_aleatory_user):
    
    response = create_aleatory_user
    
    assert response.status_code == 200
    
    user = response.json()

    assert user["name"] is not None
    assert user["email"] is not None    
    
    logger.info("1. Test of user creation passed successfully.")
    logger.info(f"User created: {user}") 
    
    

def test_list_users(client):

    response = client.get("/users/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0



def test_get_user(client, create_aleatory_user):
    user = create_aleatory_user
    response = client.get(f"/users/{user['id']}")

    assert response.status_code == 200


def test_delete_user(client, create_aleatory_user):
    
    user = create_aleatory_user
    response = client.delete(f"/users/{user['id']}")
    
    assert response.status_code == 200
    
    response = client.get(f"/users/{user['id']}")   
    assert response.status_code == 404


def test_update_user(client, create_aleatory_user):
    user = create_aleatory_user
    response = client.patch(f"/users/{user['id']}", json={"password": "98765"})
    
    assert response.status_code == 200

