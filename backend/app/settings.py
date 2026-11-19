from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["local", "test", "production"]


class EnvironmentSettings(BaseSettings):
    """Only the name of the environment.

    It needs nothing else, so logging can be set up before the rest of the
    settings are checked. That way even a "missing setting" error at start-up
    is written in the normal log format.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: Environment = "local"


class Settings(EnvironmentSettings):
    """Every setting the backend reads, filled from the environment.

    Values come from real environment variables first, then from a local
    `.env` file. A missing required value stops the app at startup.
    """

    # Required, no default. The URL contains a password, so it is a secret.
    database_url: SecretStr


@lru_cache
def get_settings() -> Settings:
    """Create the settings once, then reuse them."""
    return Settings()  # pyright: ignore[reportCallIssue]
