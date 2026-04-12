from api.db.models.user_model import User
from utils.logger import logger

def test_create_user_duplicate_email(client, existing_user):
    user = existing_user
    response = client.post("/users/", json=user)

    assert response.status_code == 409
    
    logger.info("1. Test of creation of invalid user with duplicated email passed successfully.")
    
    
def test_invalid_password(client):
    user = {"name": "Test User","email": "test@example.com","password": "short" }
    
    response = client.post("/users/", json=user)
    assert response.status_code == 422
    
    logger.info(user)
    logger.info("2. Test of creation of invalid user with duplicated email passed successfully.")

    
def test_get_user_not_found(client):
    response = client.get("/users/9999")
    
    assert response.status_code == 404
    
    logger.info("3. Test of get unregistered user passed successfully.")
    

def test_create_user_with_invalid_payload(client):
    response = client.post("/users/", json={"name": "Test"})  # faltando campos
    assert response.status_code == 422
    
    logger.info("4.1. Test with invalid payload passed successfully (Least than expected)")
    
    response = client.post("/users/", json={"name": "Existing", "email": "existing@example.com", "password": "password", "age": 30, "gender": "Male"})  # campos a mais
    assert response.status_code == 422
    
    logger.info("4.2. Test with invalid payload passed successfully (More than expected)")
    


def test_delete_user_not_found(client):
    response = client.delete("/users/9999")
    assert response.status_code == 404
    
    logger.info("5. Test of delete unregistered user passed successfully.")

def test_update_user_not_found(client):
    response = client.patch("/users/9999", json={"name": "Updated"})
    assert response.status_code == 404

    logger.info("6. Test of update unregistered user passed successfully.")
