from fastapi import status, APIRouter, Depends, HTTPException, Path, Request
from typing import Annotated
from backend.routers.auth import get_current_user
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from backend.models.models import Todos
from backend.database.database import db_dependency

templates = Jinja2Templates(directory="./backend/templates")


router = APIRouter(prefix="/todos", tags=["todos"])

user_dependency = Annotated[dict, Depends(get_current_user)]


def redirect_to_login():
    redirect_response = RedirectResponse(
        url="/login-page", status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        todos = db.query(Todos).filter(Todos.owner_id == user.get("user_id")).all()
        return templates.TemplateResponse(
            "todo.html", {"request": request, "todos": todos, "user": user}
        )
    except:
        return redirect_to_login()


@router.get("/add-todo-page")
async def render_add_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse(
            "add-todo.html", {"request": request, "user": user}
        )
    except:
        return redirect_to_login()


@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, 
                                db: db_dependency,  todo_id: int = Path(gt=0)):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        return templates.TemplateResponse(
            "edit-todo.html", {"request": request, "todo": todo, "user": user}
        )
    except:
        return redirect_to_login()


class TodoRequest(BaseModel):
    title: str = Field(...,min_length=3)
    description: str = Field(...,min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    model_config = {
        "json_schema_extra": {
            "example": {
               "title": "first todo",
               "description": "first todo description",
               "priority": 1,
               "complete": True
            }
        }
    }


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
