# 0008. Pytest as the test runner

- **Status:** Accepted
- **Date:** 2026-11-16

## Context

Retainly's money maths must be provably correct, and most code is written by an AI assistant. A linter ([0006](0006-ruff-linter-formatter.md)) checks style and a type checker ([0007](0007-pyright-strict-type-checker.md)) checks types. Tests check **behaviour**. From M4 the same tool also runs the evals that grade AI features.

## Options considered

1. **unittest.** Built into Python. Class-based and wordy.
2. **pytest.** The community standard. Plain functions, plain `assert`, fixtures, parametrized tests, plugins. FastAPI's own documentation uses it.
3. **Older runners (nose and others).** Largely abandoned.

## Decision

- **pytest** is the test runner.
- Tests live in `backend/tests/`. Files and functions start with `test_`.
- Run with `uv run pytest`.
- The plugin for async tests (pytest-asyncio or anyio) is decided when the first async test appears.

## How often tests run

- **After every change (the AI assistant):** ruff, pyright and the tests covering the touched code. The aim is a few seconds.
- **Before each commit (pre-commit):** ruff, pyright and the fast tests only.
- **On every push (CI):** the full suite, including slow tests such as those that need PostgreSQL in Docker. CI is the one that enforces the rules.
- **Evals (from M4):** they call a real model, so they cost money and time. They run in CI on changes that touch AI code, or on request, not after every edit.

If the suite becomes slow, tests are split into fast and slow groups with pytest markers.

## Consequences

- Money maths gets exact tests, with parametrized tables for VAT, rounding and currency cases.
- FastAPI's test client calls routes without starting a server.
- Fixtures are found by parameter name. This feels unusual coming from Swift and needs practice.
- A weak test can pass while the code is wrong, for example an AI-written test that repeats the code's own logic. Tests must be reviewed, and ideally seen to fail once.
- Passing tests show the code matches what the tests check, not that it is correct.
- A coverage number shows what ran, not what was checked. We do not chase a percentage.

## What to learn

- A test runner finds tests, runs each separately and reports failures with the values that differ.
- A linter, a type checker and a test catch different things: style, types and behaviour.
- A fixture is reusable setup that a test asks for by name. It is like `setUp()` in XCTest, chosen per test.
- Parametrized tests run one test over many inputs, which suits money maths.
- Passing tests are evidence, not proof.
