from fastapi import FastAPI, APIRouter, Depends, status, HTTPException
from database.database import db_dependency
from routers.auth import get_current_user
from typing import Annotated
from models.models import Users, Todos


router = APIRouter(prefix="/admin", tags=["admin"])
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_users(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).all()


@router.delete("/{username}", status_code=status.HTTP_200_OK)
async def delete_user(username: str, user: user_dependency, db: db_dependency):

    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    db.query(Users).filter(user.get("username") == username).delete()
    db.commit()
    return {"detail": "user is deleted successfully"}


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).all()
