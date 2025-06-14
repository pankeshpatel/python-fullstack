from fastapi import FastAPI, status
from routers import auth, todos, admin, users, health
from database.database import engine, Base


app = FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(health.router)
