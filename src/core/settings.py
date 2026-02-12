from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    MONGO_URI: str
    MONGO_DATABASE_NAME: str = "case"
    MONGO_COLLECTION_MODELS: str = "models"
    MONGO_COLLECTION_PREDICTIONS: str = "predictions"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()  # type: ignore
