import pytest


def test_create_user(playwright):
    # cria contexto de request
    request = playwright.request.new_context()

    # payload correto (dict normal)
    user = {
        "name": "User3",
        "email": "e2e@example.com",
        "password": "12345678"
    }

    # 🚀 envio correto (SEM json.dumps e SEM headers manual)
    response = request.post(
        "http://localhost:8000/users/",
        data=user
    )

    # debug útil
    print("STATUS:", response.status)
    print("BODY:", response.text())

    # validação
    assert response.status == 201