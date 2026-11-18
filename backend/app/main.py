from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Literal

import structlog
from fastapi import FastAPI
from pydantic import BaseModel

from app.logging_config import configure_logging
from app.middleware import RequestContextMiddleware
from app.settings import get_settings

log: structlog.stdlib.BoundLogger = structlog.get_logger()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """Runs once when the server starts. Bad settings stop the app here."""
    settings = get_settings()
    configure_logging(settings.environment)
    log.info("app_started", environment=settings.environment)
    yield


app = FastAPI(title="Retainly API", lifespan=lifespan)
app.add_middleware(RequestContextMiddleware)


class HealthResponse(BaseModel):
    """The shape of the reply from GET /health."""

    status: Literal["ok"]


@app.get("/health")
def health() -> HealthResponse:
    """Say that the service is up. Used by Docker, CI and monitoring."""
    return HealthResponse(status="ok")
