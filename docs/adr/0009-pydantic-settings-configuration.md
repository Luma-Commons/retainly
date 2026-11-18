# 0009. Pydantic-settings for configuration

- **Status:** Accepted
- **Date:** 2026-11-17

## Context

The backend needs values that differ between places: the database address, secrets such as the Anthropic API key, and switches such as the environment name. The repository is public, so secrets must never be written in code. Values read ad hoc from the environment are plain strings, and a missing or mistyped one fails late and confusingly.

## Options considered

1. **`os.environ` by hand.** Built in. Strings only, no checking, and the type checker cannot see which settings exist.
2. **python-dotenv.** Loads a `.env` file into the environment. Loading only: no types, no checks.
3. **pydantic-settings.** A Pydantic model whose fields are filled from the environment. Types, defaults and validation in one place. A separate package from Pydantic.
4. **Dynaconf and other configuration frameworks.** More than this project needs.

## Decision

- **pydantic-settings** for all configuration.
- One `Settings` class in `backend/app/settings.py`, created once and cached.
- Values come from the environment. A local `.env` file is a development convenience and is **never committed**.
- Secrets use `SecretStr` and have **no default**, so a missing secret stops the app from starting.
- The app reads its settings when it starts, so a bad configuration fails at once with a clear message.
- `.env.example` lists every setting name with a placeholder value and is kept in step with the class.
- Settings are added when the feature that needs them arrives. In M0 these are `ENVIRONMENT` and `DATABASE_URL`. The Anthropic key is added in M4.

## Consequences

- The same code runs on a laptop, in CI and in production, with each place supplying its own values.
- A missing or wrongly typed value stops the app at startup, not an hour later.
- `SecretStr` prints as `**********`, so a secret is less likely to leak into logs.
- It is one more dependency.
- Nested settings need a naming convention that takes learning.
- A `.env` file on a laptop is still a file full of secrets. `.gitignore` and gitleaks are safety nets, not guarantees.
- Tests must set the values they need (for example with `monkeypatch`) instead of relying on a developer's `.env`.

## What to learn

- An environment variable is a named value that lives outside the code, in the place the program runs.
- Secrets and addresses do not belong in code, especially in a public repository.
- Failing at startup is better than failing late.
- A settings class is a Pydantic model, like `Codable` with validation.
- Mobile apps never hold the Anthropic key. It lives only on the backend.
