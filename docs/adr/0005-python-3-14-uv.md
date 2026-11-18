# 0005. Python 3.14 with uv

- **Status:** Accepted
- **Date:** 2026-11-16

## Context

The backend (see [0004](0004-python-fastapi-backend.md)) needs a Python version, a place to keep each project's libraries separate from the system Python, and a way to get the exact same library versions on a laptop, in CI and in Docker. In Swift, Xcode and Swift Package Manager answer this. In Python the author picks the tools.

## Options considered

**Tool**

1. **pip + venv.** Built in and simple. We assemble everything ourselves, and there is no real lock file.
2. **Poetry.** Mature all-in-one manager. Slower, with its own conventions.
3. **uv.** One fast tool that installs Python versions, creates the environment, adds libraries, writes a lock file and runs commands. Uses the standard `pyproject.toml`.
4. **pdm / Hatch.** Capable all-in-one tools with smaller communities.

**Python version** (checked on 2026-11-16)

1. **3.15** (3.15.2, released 2026-10-09). Newest, but about five weeks old, so some libraries may not support it yet.
2. **3.14** (3.14.10, released 2025-10-07). Over a year old, bug fixes until 2027-10, security fixes until 2030-10.
3. **3.13.** Its bug-fix period ended in 2026-10, so it only gets security fixes now.

## Decision

- **Python 3.14**, installed and pinned by uv.
- **uv** for libraries, virtual environments and the lock file.
- **`pyproject.toml`** as the single project file.
- **`uv.lock` is committed** to the repository.

## Consequences

- One tool covers Python install, environment, dependencies, lock and running commands.
- Every machine and CI run installs identical versions with `uv sync`.
- `uv.lock` is uv's own format. Moving to another tool later means regenerating the lock from `pyproject.toml`. The dependency list itself stays portable.
- uv is newer than pip and Poetry. Its commands may change faster, and many tutorials show the older tools, so commands need translating.
- uv must be installed on each machine, in CI and in the Dockerfile.
- Moving to 3.15 later is a small change: edit the version line and re-lock. We revisit it once the libraries we use support it.
- A standard lock-file format (`pylock.toml`) has been proposed. We check how far uv supports it when we set the project up.

## What to learn

- Never install libraries into the system Python. A virtual environment gives each project its own private copy.
- `pyproject.toml` says what we want (for example "FastAPI 0.1xx or newer"). The lock file records exactly what was installed.
- Committing the lock file makes builds reproducible.
- Prefer a version of a language that is mature and still receiving bug fixes, not necessarily the newest.
