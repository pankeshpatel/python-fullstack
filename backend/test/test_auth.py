from .utils import (
    client,
    test_user,
    override_get_db,
    override_get_current_user,
    TestingSessionLocal,
    test_todo,
)
from fastapi import status, HTTPException
from backend.main import app
from backend.models.models import Users, Todos

from backend.routers.auth import (
    authenticate_user,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
    get_current_user,
)


from backend.database.database import get_db
from datetime import timedelta
from jose import jwt
import pytest


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username


def test_wrong_username(test_user):
    db = TestingSessionLocal()
    wrong_username_user = authenticate_user("WrongUserName", "testpassword", db)
    assert wrong_username_user is False


def test_wrong_password(test_user):
    db = TestingSessionLocal()
    wrong_password_user = authenticate_user(test_user.username, "wrongpassword", db)
    assert wrong_password_user is False


def test_create_access_token():
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decoded_token["username"] == username
    assert decoded_token["user_id"] == user_id
    assert decoded_token["user_role"] == role


@pytest.mark.asyncio
async def test_get_current_user():
    encode = {"username": "testuser", "user_id": 1, "user_role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token)
    assert user == {"username": "testuser", "user_id": 1, "user_role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"user_role": "testuser"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "could not validate user"
