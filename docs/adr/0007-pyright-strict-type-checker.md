# 0007. Pyright in strict mode for type checking

- **Status:** Accepted
- **Date:** 2026-11-16

## Context

Python reads type hints but ignores them when the code runs. Without a separate tool, wrong types are found only when a line fails. Pydantic ([0004](0004-python-fastapi-backend.md)) checks data coming in from outside while the program runs. A static type checker checks that our own code fits together, before it runs, like the Swift compiler.

Most code here is written by an AI assistant, and money maths needs exact types (integer minor units plus a currency). A checker proves in seconds that code the author did not type is consistent.

## Options considered

Findings are from web sources read on 2026-11-16. They were not tested on this code, and the conformance figures vary by source and date.

1. **mypy.** Stable since 2012, version 2.0 in May 2026. Most tutorials and plugins. The slowest option.
2. **Pyright (Microsoft).** Stable since 2019. Very accurate, with a strong strict mode and clear messages. Needs a Node.js runtime, which the Python package downloads.
3. **Pyrefly (Meta).** Stable 1.0 since 2026-05-12. Written in Rust, very fast, newer.
4. **ty (Astral).** Still in beta. Rust, very fast, same company as uv and ruff.

## Decision

- **Pyright** in **strict mode**, from the first line of code.
- Config in `pyproject.toml`.
- Runs in **pre-commit** and **CI**. CI is the one that enforces it.
- The AI assistant runs it after every change.

## Consequences

- Wrong types, missing `None` checks and wrong arguments are found before running or testing.
- Strict mode gives many errors at first, mostly around libraries without type hints. Starting strict on a new project is easier than tightening an old one later.
- Pyright needs Node.js, which its Python package downloads. This is an odd dependency in a Python project.
- It is slower than Pyrefly and ty. The project is small, so this is not expected to matter.
- Switching checkers later is cheap. They read the same hints, so only the config changes. We revisit when ty reaches 1.0 or if the Node dependency becomes a problem. Pyrefly is the runner-up.
- Pydantic and the type checker do different jobs and both stay: Pydantic guards the edges at runtime, the checker guards the inside before runtime.

## What to learn

- A type hint is a note. Python ignores it when running, and a type checker reads it.
- A checker works without running the code.
- Pydantic checks data at runtime. A checker checks code before runtime.
- Strict mode means every function is hinted and unknown types are errors.
- A checker is a cheap, fast check on AI-written code.
