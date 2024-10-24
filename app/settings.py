from fastapi import Path
from fastapi_mail import ConnectionConfig
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings

# from pathlib import Path


class Settings(BaseSettings):
    # DB Settings
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "foodics"
    DB_URL: str = ""

    # Email Settings
    SENDGRID_API_KEY: str
    FROM_EMAIL: str
    MERCHANT_EMAIL: str

    @field_validator("DB_URL")
    @classmethod
    def assemble_db_url(cls, db_url: str, info: ValidationInfo) -> str:
        if db_url:
            return db_url
        data = info.data
        return f"postgresql://{data["DB_USER"]}:{data["DB_PASSWORD"]}@{data["DB_HOST"]}:{data["DB_PORT"]}/{data["DB_NAME"]}"


settings = Settings()
