from utils.logger import logger

def test_create_user(client, create_aleatory_user):
    
    response = create_aleatory_user
    
    assert response.status_code == 201
    
    user = response.json()

    assert user["name"] is not None
    assert user["email"] is not None    
    
    logger.info("1. Test of user creation passed successfully.")
    logger.info(f"User created: {user}") 
    
    

def test_list_users(client):

    response = client.get("/users/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    #assert len(response.json()) > 0
    
    logger.info("2. Test of user listing passed successfully.")
    logger.info(f"Users list: {response}") 
    
    
    # assert response.status_code == 200
    # data = response.json()

    # assert isinstance(data, list)
    # assert len(data) > 0



def test_get_user(client, create_aleatory_user):
    user = create_aleatory_user.json()
    response = client.get(f"/users/{user['id']}")

    assert response.status_code == 200
    
    logger.info("3. Test of user retrieval passed successfully.")
    logger.info(f"User created: {user}") 


def test_delete_user(client, create_aleatory_user):
    
    user = create_aleatory_user.json()
    response = client.delete(f"/users/{user['id']}")
    
    assert response.status_code == 204
    
    response = client.get(f"/users/{user['id']}")   
    assert response.status_code == 404
    
    logger.info("4. Test of user deletion passed successfully.")


def test_update_user(client, create_aleatory_user):
    user = create_aleatory_user.json()
    response = client.patch(f"/users/{user['id']}", json={"email": "atualizado@teste.com"})
    
    assert response.status_code == 200
    
    logger.info("5. Test of user update passed successfully.")
    logger.info(f"User created: {user}") 

