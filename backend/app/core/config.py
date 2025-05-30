"""
Loads environment-based configuration settings (e.g., database URL) using Pydantic for global app access.
"""

from pydantic_settings import BaseSettings 


class Settings(BaseSettings):
    # Define your expected environment variables here
    DATABASE_URL: str

    class Config:
        env_file = ".env"

# Create a global settings object to be used across the app
settings = Settings()