from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Every setting the backend reads, filled from the environment.

    Values come from real environment variables first, then from a local
    `.env` file. A missing required value stops the app at startup.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: Literal["local", "test", "production"] = "local"
    # Required, no default. The URL contains a password, so it is a secret.
    database_url: SecretStr


@lru_cache
def get_settings() -> Settings:
    """Create the settings once, then reuse them."""
    return Settings()  # pyright: ignore[reportCallIssue]
