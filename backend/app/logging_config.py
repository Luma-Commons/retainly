import logging
import sys

import structlog
from structlog.typing import EventDict, Processor, WrappedLogger

from app.settings import Environment, EnvironmentSettings

# Keys whose values must never reach the logs. A safety net: the real rule is
# not to log secrets in the first place.
SENSITIVE_KEYS = frozenset(
    {
        "password",
        "api_key",
        "authorization",
        "cookie",
        "token",
        "secret",
        "database_url",
    }
)


def redact_sensitive(
    _logger: WrappedLogger, _method: str, event_dict: EventDict
) -> EventDict:
    """A processor: replace the value of any sensitive key with ***."""
    for key in event_dict:
        if key.lower() in SENSITIVE_KEYS:
            event_dict[key] = "***"
    return event_dict


def _shared_processors() -> list[Processor]:
    """Steps every log line goes through, whoever wrote it."""
    return [
        structlog.contextvars.merge_contextvars,  # adds request_id etc.
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        redact_sensitive,
    ]


def build_formatter(environment: Environment) -> structlog.stdlib.ProcessorFormatter:
    """The formatter that turns any standard log record into our format."""
    # The last step decides the format.
    final: list[Processor] = [
        structlog.stdlib.ProcessorFormatter.remove_processors_meta
    ]
    if environment == "local":
        final.append(structlog.dev.ConsoleRenderer())
    else:
        final.append(structlog.processors.format_exc_info)
        final.append(structlog.processors.JSONRenderer())

    return structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=_shared_processors(),  # for lines from other libraries
        processors=final,
    )


def uvicorn_formatter() -> structlog.stdlib.ProcessorFormatter:
    """Factory used by Uvicorn's log config file (app/uvicorn_logging.json).

    Uvicorn sets up its logging before our app starts, so this reads only the
    environment name and does not need the other settings.
    """
    return build_formatter(EnvironmentSettings().environment)


def configure_logging(environment: Environment) -> None:
    """Set up structlog and route standard logging (Uvicorn) through it."""
    structlog.configure(
        processors=[
            *_shared_processors(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=False,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(build_formatter(environment))

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)

    # Uvicorn writes through the same handler. Its access log is off because
    # our middleware writes one summary line per request.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        library_logger = logging.getLogger(name)
        library_logger.handlers = []
        library_logger.propagate = True
    logging.getLogger("uvicorn.access").disabled = True

    # HTTP client libraries log the full URL of every request at INFO level,
    # query string included. That can leak personal data, so only warnings
    # and errors get through.
    for name in ("httpx", "httpx2", "httpcore", "httpcore2"):
        logging.getLogger(name).setLevel(logging.WARNING)
