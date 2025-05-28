# app/core/config.py

from pydantic_settings import BaseSettings  # <-- correct for Pydantic v2


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()