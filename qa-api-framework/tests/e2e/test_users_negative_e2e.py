from utils.logger import logger

def test_get_user_not_found(api_request):

    response = api_request.get("/users/999999")
    
    data = response.json()

    assert response.status == 404
    assert data["detail"] == "User not found"

    logger.info("6. User not found validated")


def test_create_duplicate_email(api_request):

    response = api_request.post(
        "/users/",
        data={
            "name": "Outro Usuario",
            "email": "e2e@example.com",
            "password": "12345678"
        }
    )
    
    data = response.json()

    assert response.status == 409
    assert data["detail"] == "Email already exists"

    logger.info("7. Duplicate email blocked")
    
    
def test_missing_parameters(api_request, create_aleatory_user):
    user = create_aleatory_user.json()

    response = api_request.post(
        "/users/",
        data={
            "name": "Outro Usuario",
            "email": user["email"],
        }
    )
    
    data = response.json()

    assert response.status == 422
    assert data["detail"][0]["type"] == "missing"
    assert data["detail"][0]["msg"] == "Field required"