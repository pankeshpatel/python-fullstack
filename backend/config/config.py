import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class AppEnvs(Enum):
    LOCAL = "local"
    DEVELOPMENT = "dev"
    QA = "qa"
    TEST = "test"
    PRODUCTION = "prod"



class Settings(BaseSettings):

    #POSTGRESQL
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_DB: str 
    POSTGRES_SERVER: str 
    POSTGRES_PORT: int 

    # Redis
    REDIS_HOST: str = ""
    REDIS_PORT: str = ""
    REDIS_PASSWORD: str = ""

    # JWT
    SECRET_KEY: str
    ALGORITHM: str

    ENVIRONMENT: AppEnvs = AppEnvs.LOCAL



    model_config = SettingsConfigDict(
        env_file=f"./backend/.env.local",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )


    # model_config = SettingsConfigDict(
    #     env_file=f"./backend/.env.dev",
    #     env_file_encoding="utf-8",
    #     extra="ignore",
    #     case_sensitive=True
    # )
    


settings = Settings()