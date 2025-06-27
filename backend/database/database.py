from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
import os
from backend.config.config import settings







# sqlite connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./backend/database/todosapp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]



# def get_url():
#     user =  settings.POSTGRES_USER  
#     password = settings.POSTGRES_PASSWORD   
#     server =  settings.POSTGRES_SERVER 
#     port = settings.POSTGRES_PORT 
#     db = settings.POSTGRES_DB 
#     return f"postgresql://{user}:{password}@{server}:{port}/{db}"



# if settings.ENVIRONMENT == "dev":
#     SQLALCHEMY_DATABASE_URL = get_url()
#     engine = create_engine(SQLALCHEMY_DATABASE_URL)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     Base = declarative_base()




# postgres_engine = create_engine(POSTGRES_DATABASE_URL)
# postgress_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# postgres_base = declarative_base()



# prod
# SQLALCHEMY_DATABASE_URL = (
#     "postgresql://postgres:postgres@localhost/TodoApplicationDatabase"
# )
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
