from fastapi.testclient import TestClient
from backend.main import app
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from backend.database.database import Base
import pytest
from backend.routers.auth import bcrypt_context
from backend.models.models import Users, Todos


SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./backend/database/testdb.db"
test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "testusername", "user_id": 1, "user_role": "admin"}


client = TestClient(app)


@pytest.fixture
def test_user():
    user = Users(
        username="testuser",
        first_name="test",
        last_name="user",
        hashed_password=bcrypt_context.hash("testpassword"),
        email="testuser@email.com",
        role="admin",
        phone_number="111-111-1111",
        is_active=True,
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with test_engine.connect() as connection:
        connection.execute(text("DELETE from users;"))
        connection.commit()


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with test_engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
