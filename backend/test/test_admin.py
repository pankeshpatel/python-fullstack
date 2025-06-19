from .utils import (
    client,
    test_user,
    override_get_db,
    override_get_current_user,
    TestingSessionLocal,
    test_todo,
)
from fastapi import status
from backend.main import app
from backend.models.models import Users, Todos


from backend.database.database import get_db
from backend.routers.admin import get_current_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated_users(test_user):
    response = client.get("/admin/")
    assert response.status_code == status.HTTP_200_OK
    print(f"Response...{response.json()}")
    assert response.json()[0]["username"] == "testuser"
    assert response.json()[0]["first_name"] == "test"
    assert response.json()[0]["last_name"] == "user"
    assert response.json()[0]["email"] == "testuser@email.com"
    assert response.json()[0]["phone_number"] == "111-111-1111"


def test_admin_delete_user_authenticated(test_user):
    response = client.delete("/admin/testuser")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "user is deleted successfully"}


def test_adimin_read_all_todos_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["title"] == "Learn to code!"
    assert response.json()[0]["priority"] == 5
