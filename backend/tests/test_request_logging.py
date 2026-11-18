import json
import logging
import re
from collections.abc import Iterator
from typing import Any

import pytest
import structlog
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.logging_config import configure_logging
from app.middleware import (
    REQUEST_ID_HEADER,
    RequestContextMiddleware,
    accept_or_create_request_id,
)

log: structlog.stdlib.BoundLogger = structlog.get_logger()


@pytest.fixture(autouse=True)
def restore_logging() -> Iterator[None]:
    """Logging settings are global, so put them back after every test."""
    root = logging.getLogger()
    saved_handlers, saved_level = root.handlers[:], root.level
    yield
    root.handlers, root.level = saved_handlers, saved_level
    logging.getLogger("uvicorn.access").disabled = False
    for name in ("httpx", "httpx2", "httpcore", "httpcore2"):
        logging.getLogger(name).setLevel(logging.NOTSET)
    structlog.reset_defaults()


@pytest.fixture
def client() -> TestClient:
    """A tiny app with only our middleware and one route that logs."""
    app = FastAPI()
    app.add_middleware(RequestContextMiddleware)

    @app.get("/work")
    def work() -> dict[str, str]:  # pyright: ignore[reportUnusedFunction]
        # This function is never given the request ID, yet the line has it.
        log.info("inside_handler", contract_id=42)
        return {"ok": "yes"}

    return TestClient(app)


def json_lines(captured: str) -> list[dict[str, Any]]:
    return [json.loads(line) for line in captured.splitlines() if line.startswith("{")]


def find(lines: list[dict[str, Any]], event: str) -> dict[str, Any]:
    return next(line for line in lines if line["event"] == event)


# --- the ID itself -----------------------------------------------------------


def test_an_id_is_created_when_none_is_sent() -> None:
    request_id = accept_or_create_request_id(None)

    assert re.fullmatch(r"[0-9a-f]{32}", request_id)


def test_a_safe_incoming_id_is_reused() -> None:
    assert accept_or_create_request_id("app-request_123.abc") == "app-request_123.abc"


@pytest.mark.parametrize(
    "bad",
    [
        "short",  # too short
        "x" * 65,  # too long
        "has space in it",
        "line\nbreak-attack",
        "semi;colon;chars",
        "",
    ],
)
def test_an_unsafe_incoming_id_is_replaced(bad: str) -> None:
    request_id = accept_or_create_request_id(bad)

    assert request_id != bad
    assert re.fullmatch(r"[0-9a-f]{32}", request_id)


# --- the middleware ----------------------------------------------------------


def test_the_id_is_returned_in_the_response_header(client: TestClient) -> None:
    response = client.get("/work")

    assert re.fullmatch(r"[0-9a-f]{32}", response.headers[REQUEST_ID_HEADER])


def test_a_safe_id_from_the_caller_comes_back_unchanged(client: TestClient) -> None:
    response = client.get("/work", headers={REQUEST_ID_HEADER: "from-the-app-001"})

    assert response.headers[REQUEST_ID_HEADER] == "from-the-app-001"


def test_each_request_gets_its_own_id(client: TestClient) -> None:
    first = client.get("/work").headers[REQUEST_ID_HEADER]
    second = client.get("/work").headers[REQUEST_ID_HEADER]

    assert first != second


def test_every_line_of_a_request_carries_the_same_id(
    client: TestClient, capsys: pytest.CaptureFixture[str]
) -> None:
    configure_logging("production")

    response = client.get("/work")
    lines = json_lines(capsys.readouterr().out)
    request_id = response.headers[REQUEST_ID_HEADER]

    assert find(lines, "inside_handler")["request_id"] == request_id
    assert find(lines, "request_finished")["request_id"] == request_id


def test_the_summary_line_has_method_path_status_and_duration(
    client: TestClient, capsys: pytest.CaptureFixture[str]
) -> None:
    configure_logging("production")

    client.get("/work")
    summary = find(json_lines(capsys.readouterr().out), "request_finished")

    assert summary["method"] == "GET"
    assert summary["path"] == "/work"
    assert summary["status"] == 200
    assert isinstance(summary["duration_ms"], float)


def test_the_query_string_is_never_logged(
    client: TestClient, capsys: pytest.CaptureFixture[str]
) -> None:
    configure_logging("production")

    client.get("/work?client_email=someone@example.com")
    output = capsys.readouterr().out

    assert "someone@example.com" not in output
    assert "client_email" not in output


def test_one_request_id_does_not_leak_into_the_next(
    client: TestClient, capsys: pytest.CaptureFixture[str]
) -> None:
    configure_logging("production")

    first = client.get("/work").headers[REQUEST_ID_HEADER]
    second = client.get("/work").headers[REQUEST_ID_HEADER]
    lines = json_lines(capsys.readouterr().out)

    finished = [line for line in lines if line["event"] == "request_finished"]
    assert [line["request_id"] for line in finished] == [first, second]


# --- the logging setup -------------------------------------------------------


def test_sensitive_values_are_replaced(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging("production")

    log.info("login_attempt", password="hunter2", api_key="sk-secret", user_id=7)
    line = find(json_lines(capsys.readouterr().out), "login_attempt")

    assert line["password"] == "***"
    assert line["api_key"] == "***"
    assert line["user_id"] == 7


def test_uvicorn_log_lines_use_the_same_format(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging("production")

    logging.getLogger("uvicorn.error").info("Started server process")
    line = find(json_lines(capsys.readouterr().out), "Started server process")

    assert line["level"] == "info"
    assert "timestamp" in line


def test_local_environment_prints_readable_lines_not_json(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging("local")

    log.info("hello_local")
    output = capsys.readouterr().out

    assert "hello_local" in output
    assert not output.lstrip().startswith("{")
