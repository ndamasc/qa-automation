def test_create_user_duplicate_email(client):
    
    user = {"name": "Test", "email": "invalido@example.com", "password": "password"}
    response = client.post("/users/", json=user)

    assert response.status_code in [400, 409]
    
    
def test_get_user_not_found(client):
    response = client.get("/users/9999")
    assert response.status_code == 404
    

def test_create_user_invalid_payload(client):
    response = client.post("/users/", json={"name": "Test"})  # faltando campos
    assert response.status_code == 422
    

def test_delete_user_not_found(client):
    response = client.delete("/users/9999")
    assert response.status_code == 404

def test_update_user_not_found(client):
    response = client.patch("/users/9999", json={"name": "Updated"})
    assert response.status_code == 404
