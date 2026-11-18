from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from app.settings import Settings, get_settings

FAKE_URL = "postgresql://user:s3cret@localhost:5432/test"


@pytest.fixture(autouse=True)
def clean_settings(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Make every test independent of the developer's real settings."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.chdir(tmp_path)  # so no real .env file is found
    get_settings.cache_clear()


def test_settings_are_read_from_the_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", FAKE_URL)
    monkeypatch.setenv("ENVIRONMENT", "test")

    settings = Settings()  # pyright: ignore[reportCallIssue]

    assert settings.environment == "test"
    assert settings.database_url.get_secret_value() == FAKE_URL


def test_environment_defaults_to_local(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", FAKE_URL)

    settings = Settings()  # pyright: ignore[reportCallIssue]

    assert settings.environment == "local"


def test_missing_database_url_is_an_error() -> None:
    with pytest.raises(ValidationError):
        Settings()  # pyright: ignore[reportCallIssue]


def test_unknown_environment_is_an_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", FAKE_URL)
    monkeypatch.setenv("ENVIRONMENT", "staging-ish")

    with pytest.raises(ValidationError):
        Settings()  # pyright: ignore[reportCallIssue]


def test_the_secret_does_not_appear_in_printed_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", FAKE_URL)

    settings = Settings()  # pyright: ignore[reportCallIssue]

    assert "s3cret" not in str(settings)
    assert "s3cret" not in repr(settings)


def test_app_refuses_to_start_without_settings() -> None:
    with pytest.raises(ValidationError):
        with TestClient(app):
            pass


def test_app_starts_when_settings_are_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", FAKE_URL)

    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
