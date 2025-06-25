from fastapi import APIRouter, status, Depends, HTTPException, Path
from backend.database.database import db_dependency
from backend.models.models import Users
from pydantic import BaseModel, Field, EmailStr, field_validator
from passlib.context import CryptContext
from typing import Annotated
from backend.routers.auth import get_current_user
import re


router = APIRouter(prefix="/user", tags=["user"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_dependency = Annotated[dict, Depends(get_current_user)]

PHONE_REGEX = re.compile(r"^\+?1?\d{10,15}$")



class CreateUserRequest(BaseModel):
    username: str = Field(..., description="Unique username for the user", min_length=3, max_length=50),
    email: EmailStr = Field(description="Valid email address")
    first_name: str = Field(description="User's first name", min_length=1, max_length=50)
    last_name: str = Field(description="User's last name", min_length=1, max_length=50)
    password: str = Field(..., description="Password with at least 8 characters", min_length=8)
    role: str = Field(description="Role assigned to the user")
    phone_number: str = Field(description="User's phone number", min_length=10, max_length=15)

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]{2,19}$", value):
            raise ValueError("Username must start with a letter and contain only letters, numbers, and underscores (3–20 characters).")
        return value

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "test_user",
                "email": "test.user@email.com",
                "first_name" : "test",
                "last_name" : "user",
                "password" : "test_user_password",
                "role" : "admin",
                "phone_number": "111-111-1111"
            }
        }
    }


class UserVerification(BaseModel):
    password: str = Field(..., min_length=8)
    new_password: str = Field( ...,min_length=8)


    model_config = {
        "json_schema_extra": {
            "example": {
                "password": "old_password",
                "new_password": "new_password"
            }
        }
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get("user_id")).first()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):

    create_user = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True,
        phone_number=create_user_request.phone_number,
    )

    db.add(create_user)
    db.commit()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if not bcrypt_context.verify(
        user_verification.password, user_model.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Error on password change")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phonenumber(
    user: user_dependency, db: db_dependency, phone_number: str = Path(...,description="Phone number")
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
