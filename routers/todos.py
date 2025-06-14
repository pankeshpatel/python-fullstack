from fastapi import status, APIRouter, Depends, HTTPException, Path
from database.database import db_dependency
from typing import Annotated
from routers.auth import get_current_user
from models.models import Users, Todos
from pydantic import BaseModel, Field


router = APIRouter(prefix="/todos", tags=["todos"])

user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).filter(user.get("user_id") == Todos.owner_id).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="item not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    db: db_dependency, user: user_dependency, todo_request: TodoRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("user_id"))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency,
    user: user_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get("user_id")
    ).delete()
    db.commit()
