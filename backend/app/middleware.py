import re
import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

REQUEST_ID_HEADER = "X-Request-ID"

# An incoming ID is accepted only if it is short and made of plain characters.
# Anything else (very long, spaces, newlines) is replaced by one we create.
_SAFE_REQUEST_ID = re.compile(r"[A-Za-z0-9._-]{8,64}")

log: structlog.stdlib.BoundLogger = structlog.get_logger()


def accept_or_create_request_id(incoming: str | None) -> str:
    """Reuse a safe incoming ID, otherwise create a random one."""
    if incoming is not None and _SAFE_REQUEST_ID.fullmatch(incoming):
        return incoming
    return uuid.uuid4().hex


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Give every request an ID that appears on all of its log lines."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = accept_or_create_request_id(request.headers.get(REQUEST_ID_HEADER))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)
        started = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            log.exception(
                "request_failed",
                method=request.method,
                path=request.url.path,
            )
            raise
        else:
            response.headers[REQUEST_ID_HEADER] = request_id
            log.info(
                "request_finished",
                method=request.method,
                path=request.url.path,  # the path only, never the query string
                status=response.status_code,
                duration_ms=round((time.perf_counter() - started) * 1000, 2),
            )
            return response
        finally:
            structlog.contextvars.clear_contextvars()
