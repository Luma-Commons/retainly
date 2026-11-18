# 0010. Structlog and request IDs for logging

- **Status:** Accepted
- **Date:** 2026-11-18

## Context

When something fails on a server, logs are often the only evidence. Plain text lines are hard to search, and on a busy server lines from many requests are mixed together, so one request's story cannot be followed. Request IDs and structured logs are also the base for tracing agent and model steps later (M4 to M10) and for latency measurements (M6 and M9).

Retainly handles financial data and contracts, so what is logged matters as much as how.

## Options considered

Versions checked on PyPI on 2026-11-17. They were not tested against this code.

1. **Standard `logging` only.** Built in. JSON output and per-request fields need manual setup.
2. **structlog (26.1.0).** Structured logs with context binding built in. Works alongside standard `logging`.
3. **loguru (0.8.0).** Simple and friendly. Its own style, and less natural for per-request context.
4. **python-json-logger (4.2.0).** A JSON formatter for standard `logging`. Per-request fields are still manual.

## Decision

- **structlog** for application logs.
- **JSON** when `ENVIRONMENT` is `production` or `test`, readable coloured lines when it is `local`.
- A **middleware** that:
  - accepts an incoming `X-Request-ID` only if it is 8 to 64 characters of letters, digits, `.`, `_` or `-`, and otherwise creates a random one (a UUID4 in hex),
  - binds the ID to a context variable so every log line written during the request carries it,
  - returns the ID in the `X-Request-ID` response header,
  - writes one summary line per request with method, path (without the query string), status and duration in milliseconds,
  - clears the context when the request ends.
- A **redaction step** replaces the values of sensitive keys (for example `password`, `api_key`, `authorization`, `token`, `database_url`) with `***`.
- **Uvicorn's logs** go through the same setup, and its own access log is switched off because the middleware writes the summary line.
- The request ID is a random label. It is not a secret, holds no user information and is never used to prove who someone is.

## What must never be logged

- Secrets: API keys, passwords, tokens, database URLs.
- Contract text, bank statement content and personal data.
- Query strings, because they can carry personal data.

Log IDs (for example `contract_id`), not content. When model calls are logged (from M4), log the prompt version, token counts and timing, not the contract text.

## Consequences

- One request's whole story can be found by searching for its ID.
- Slow requests can be found by filtering on `duration_ms`.
- The same ID later ties together model calls, retrieval steps and agent steps.
- One more dependency, and a processor chain that takes learning.
- Structlog and standard `logging` run side by side, so both must be configured to write the same format.
- The redaction step is a safety net. Not logging secrets in the first place is the real rule.
- If a request fails with an unhandled error, the server's own error handler builds the 500 reply outside our middleware, so that response may not carry the `X-Request-ID` header. The failure itself is still logged with the ID.

## What to learn

- A structured log line is a record of named fields. A text log is a sentence.
- A request ID is a random tracking number for one request.
- A `ContextVar` holds a value that is separate for each request, like Swift's `@TaskLocal`. A global variable would be shared and overwritten.
- A middleware wraps every request.
- A processor is one step in structlog's chain. Each step can add, change or remove fields.
- Never trust a header from outside without checking it.
