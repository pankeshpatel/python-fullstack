from fastapi import FastAPI, status, Request
from fastapi.middleware import Middleware
from typing import List
from backend.routers import auth, todos, admin, users, health, learn
from backend.database.database import engine, Base
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import time
from backend.middleware.logging import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()
Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="./backend/static"), name="static")



@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(health.router)
app.include_router(learn.router)

# middleware

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["x-processing-time"] = str(process_time)
    return response

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

