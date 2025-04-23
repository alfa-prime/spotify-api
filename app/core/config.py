from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str

    class Config:
        env_file = ".env"
        extra = "ignore"
        encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
