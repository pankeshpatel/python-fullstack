from fastapi import FastAPI, APIRouter, Depends, status, HTTPException, Path
from backend.database.database import db_dependency
from backend.routers.auth import get_current_user
from typing import Annotated
from backend.models.models import Users, Todos


router = APIRouter(prefix="/admin", tags=["admin"])
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_users(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).all()


# @router.delete("/{username}", status_code=status.HTTP_200_OK)
# async def delete_user( user: user_dependency, db: db_dependency, 
#                       username: str = Path(...,description="Unique username for the user", min_length=3, max_length=50)):

#     if user is None or user.get("user_role") != "admin":
#         raise HTTPException(status_code=401, detail="Authentication Failed")

#     db.query(Users).filter(user.get("username") == username).delete()
#     db.commit()
#     return {"detail": "user is deleted successfully"}

from fastapi import HTTPException, Path
from sqlalchemy.exc import SQLAlchemyError

@router.delete("/{username}")
async def delete_user(
    user: user_dependency,
    db: db_dependency,
    username: str = Path(..., description="Unique username for the user", min_length=3, max_length=50)
):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    try:
        result = db.query(Users).filter(Users.username == username).delete()
        if result == 0:
            raise HTTPException(status_code=404, detail="User not found")

        db.commit()
        return {"detail": "User is deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error occurred")



@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).all()
