from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from database.database import db_dependency
from models.models import Users
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from pydantic import BaseModel


router = APIRouter(tags=["auth"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3"
ALGORITHM = "HS256"


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: str = payload.get("user_id")
        user_role: str = payload.get("user_role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                details="could not validate user",
            )
        return {"username": username, "user_id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, details="could not validate user"
        )


def create_access_token(
    username: str, user_id, user_role: str, expires_delta: timedelta
):
    encode = {"username": username, "user_id": user_id, "user_role": user_role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, details="could not validate user"
        )
    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}
