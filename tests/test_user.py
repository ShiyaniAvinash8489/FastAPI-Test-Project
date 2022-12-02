import pytest
from jose import jwt
from app.routers.user import userSchemas
from app.routers.authentication import authSchemas

from app.config import settings


# Create User
def test_create_user(client):
    res = client.post(
        "/users/create_user", json={"first_name": "Kalpesh", "last_name": "Shah", "email": "ks42238391@gmail.com", "username": "KalpeshShah09181", "phone": "+9199799899111", "password": "@Admin123"})

    # new_user = userSchemas.UserOut(**res.json())
    # assert new_user.email == "ks4223839@gmail.com"
    assert res.status_code == 201


# Login
def test_login_user(test_user, client):
    res = client.post(
        "/auth/login", {"username": test_user['response_data']["email"], "password": test_user['password']})

    login_res = authSchemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])

    id = payload.get("user_id")
    assert id == test_user['response_data']["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


# Incorrect
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 401),
    ('sanjeev@gmail.com', 'wrongpassword', 401),
    ('wrongemail@gmail.com', 'wrongpassword', 401),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/auth/login", data={"username": email, "password": password})

    assert res.status_code == status_code
