import json
import logging
import logging.config
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

BACKEND = Path(__file__).resolve().parent.parent
LOG_CONFIG = BACKEND / "app" / "uvicorn_logging.json"

UVICORN_LOGGERS = ("uvicorn", "uvicorn.error", "uvicorn.access")


@pytest.fixture(autouse=True)
def isolated_logging(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Iterator[None]:
    """Start from a clean environment, and put the global logging state back."""
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv(
        "DATABASE_URL", raising=False
    )  # Uvicorn logs before this is checked
    monkeypatch.chdir(tmp_path)  # so no real .env file is found

    root = logging.getLogger()
    saved_root = (root.handlers[:], root.level)
    saved = {
        name: (
            logging.getLogger(name).handlers[:],
            logging.getLogger(name).level,
            logging.getLogger(name).propagate,
            logging.getLogger(name).disabled,
        )
        for name in UVICORN_LOGGERS
    }
    yield
    root.handlers, root.level = saved_root
    for name, (handlers, level, propagate, disabled) in saved.items():
        logger = logging.getLogger(name)
        logger.handlers, logger.level = handlers, level
        logger.propagate, logger.disabled = propagate, disabled


def apply_uvicorn_config() -> None:
    """Do what `uvicorn --log-config app/uvicorn_logging.json` does."""
    config: dict[str, Any] = json.loads(LOG_CONFIG.read_text())
    logging.config.dictConfig(config)


def json_lines(captured: str) -> list[dict[str, Any]]:
    return [json.loads(line) for line in captured.splitlines() if line.startswith("{")]


def test_the_config_file_is_valid_json_and_names_the_uvicorn_loggers() -> None:
    config: dict[str, Any] = json.loads(LOG_CONFIG.read_text())

    assert config["version"] == 1
    assert set(UVICORN_LOGGERS) <= set(config["loggers"])


def test_uvicorn_lines_are_json_in_production(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("ENVIRONMENT", "production")
    apply_uvicorn_config()

    logging.getLogger("uvicorn.error").info("Started server process [1]")
    lines = json_lines(capsys.readouterr().out)

    assert len(lines) == 1
    assert lines[0]["event"] == "Started server process [1]"
    assert lines[0]["level"] == "info"
    assert "timestamp" in lines[0]


def test_uvicorn_lines_are_readable_locally(
    capsys: pytest.CaptureFixture[str],
) -> None:
    apply_uvicorn_config()  # ENVIRONMENT is not set, so it defaults to "local"

    logging.getLogger("uvicorn.error").info("Started server process [1]")
    output = capsys.readouterr().out

    assert "Started server process [1]" in output
    assert not output.lstrip().startswith("{")


def test_formatting_works_when_database_url_is_missing(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Uvicorn logs its first lines (and any start-up failure) before our app
    # checks DATABASE_URL, so the formatter must not need it.
    monkeypatch.setenv("ENVIRONMENT", "production")
    apply_uvicorn_config()

    logging.getLogger("uvicorn.error").info("Waiting for application startup.")

    assert json_lines(capsys.readouterr().out)[0]["event"] == (
        "Waiting for application startup."
    )


def test_a_startup_failure_traceback_becomes_a_json_field(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("ENVIRONMENT", "production")
    apply_uvicorn_config()

    try:
        raise ValueError("database_url is missing")
    except ValueError:
        logging.getLogger("uvicorn.error").exception("Exception in ASGI application")
    line = json_lines(capsys.readouterr().out)[0]

    assert line["level"] == "error"
    assert "ValueError: database_url is missing" in line["exception"]


def test_the_dockerfile_uses_a_log_config_file_that_exists() -> None:
    dockerfile = (BACKEND / "Dockerfile").read_text()

    assert '"--log-config", "app/uvicorn_logging.json"' in dockerfile
    assert (BACKEND / "app" / "uvicorn_logging.json").is_file()
    assert '"--no-access-log"' in dockerfile
