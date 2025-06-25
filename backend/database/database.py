from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
import os
from dotenv import load_dotenv

load_dotenv()


# sqlite connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./backend/database/todosapp.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]



# use this for postgres database

def get_url():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    server = os.getenv("POSTGRES_SERVER")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    return f"postgresql://{user}:{password}@{server}:{port}/{db}"

POSTGRES_DATABASE_URL = get_url()
postgres_engine = create_engine(POSTGRES_DATABASE_URL)
postgress_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
postgres_base = declarative_base()



# prod
# SQLALCHEMY_DATABASE_URL = (
#     "postgresql://postgres:postgres@localhost/TodoApplicationDatabase"
# )
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
