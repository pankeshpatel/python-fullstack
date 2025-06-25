from .utils import (
    client,
    test_user,
    override_get_db,
    override_get_current_user,
    TestingSessionLocal,
    test_todo,
)
from fastapi import status, HTTPException
from backend.models.models import Users, Todos
from backend.routers.auth import get_current_user
from backend.database.database import get_db
from datetime import timedelta
from backend.app import app


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_users_get_users(test_user):
    response = client.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "testuser"
    assert response.json()["id"] == 1


def test_change_password_success(test_user):
    response = client.put(
        "/user/password",
        json={"password": "testpassword", "new_password": "newpassword"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put(
        "/user/password",
        json={"password": "wrong_password", "new_password": "newpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_success(test_user):
    response = client.put("/user/phonenumber/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT
