from fastapi import FastAPI, status, Request
from backend.routers import auth, todos, admin, users, health, learn
from backend.database.database import engine, Base
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(health.router)
app.include_router(learn.router)
