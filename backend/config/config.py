import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    #POSTGRESQL
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_DB: str 
    POSTGRES_SERVER: str 
    POSTGRES_PORT: int 

    # JWT
    SECRET_KEY: str
    ALGORITHM: str


    model_config = SettingsConfigDict(
        env_file="./backend/.env.dev",
        case_sensitive=True
    )


settings = Settings()