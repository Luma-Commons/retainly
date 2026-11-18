# Architecture decision records

An ADR is a short note that records **one decision and why it was made**, so the reasoning is not lost. Each record lists the options that were considered and the trade-offs.

Format: see [`0000-template.md`](0000-template.md). A decision is never deleted. If it changes, a new record supersedes the old one.

| # | Decision | Status |
|---|---|---|
| [0001](0001-monorepo.md) | One monorepo | Accepted |
| [0002](0002-apache-2-license.md) | Apache-2.0 licence | Accepted |
| [0003](0003-public-from-day-one.md) | Public from day one, with safeguards | Accepted |
| [0004](0004-python-fastapi-backend.md) | Python and FastAPI for the backend | Accepted |
| [0005](0005-python-3-14-uv.md) | Python 3.14 with uv | Accepted |
| [0006](0006-ruff-linter-formatter.md) | Ruff for linting and formatting | Accepted |
| [0007](0007-pyright-strict-type-checker.md) | Pyright in strict mode for type checking | Accepted |
| [0008](0008-pytest-test-runner.md) | Pytest as the test runner | Accepted |
| [0009](0009-pydantic-settings-configuration.md) | Pydantic-settings for configuration | Accepted |
| [0010](0010-structlog-request-ids.md) | Structlog and request IDs for logging | Accepted |
| [0011](0011-qa-folder-and-collaboration.md) | QA folder and collaboration rules | Accepted |

More are added as each topic is learned and decided: backend stack (M0), Kotlin Multiplatform scope (M2), money representation (M1), and so on.
