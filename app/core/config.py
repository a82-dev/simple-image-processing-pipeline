import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Async Image & Media Pipeline"

    REDIS_URL: str = "redis://localhost:6379/0"

    UPLOAD_DIR: str = "static/uploads"
    PROCESSED_DIR: str = "static/processed"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

# checking directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.PROCESSED_DIR, exist_ok=True)
