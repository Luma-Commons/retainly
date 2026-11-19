# 0013. API container image

- **Status:** Accepted
- **Date:** 2026-11-19

## Context

The backend must run the same way on a laptop, in CI and in production, and a QA collaborator must be able to start it with one command. [0012](0012-docker-compose-postgres-18.md) decided that local development uses Docker Compose and that the API gets a Dockerfile. This record decides what that image looks like.

Facts checked on 2026-11-19:

- `python:3.14-slim` is Python 3.14.10 on Debian 13 ("trixie"). It runs as root by default and contains no `curl` or `wget`.
- An official uv image exists for the uv version used locally (0.13.0). The latest uv release is 0.13.9.

## Options considered

**Base image**

1. **`python:3.14-slim`.** Debian, pre-built Python, modest size, standard tools.
2. **`python:3.14` (full).** Much larger, with compilers we do not need.
3. **`python:3.14-alpine`.** Smaller, but it uses a different C library (musl), which some Python packages do not handle well.
4. **Distroless.** Very small and locked down, but hard to debug and more to learn.

**Build style**

1. **Multi-stage.** A builder stage installs the libraries. The final stage copies only the result.
2. **Single stage.** Simpler to read, but the final image keeps uv and build leftovers.

## Decision

- A **multi-stage Dockerfile** in `backend/`, based on **`python:3.14-slim`**.
- **uv is pinned to 0.13.0**, the version used locally. Local uv and the image are upgraded together.
- Libraries are installed with `uv sync --locked --no-dev`. The `--locked` flag fails if `uv.lock` does not match `pyproject.toml`. Development tools (ruff, pyright, pytest) are not in the image.
- **Python comes from the base image.** uv only installs libraries inside the image and does not download its own Python.
- The container runs as a **non-root user**.
- Uvicorn listens on **`0.0.0.0` inside the container**. What is reachable from outside is decided by the compose file, which publishes ports on `127.0.0.1`.
- A **health check** calls `GET /health` using Python, because the image has no `curl`.
- A **`.dockerignore`** in `backend/` keeps env files, `.venv`, caches, tests and `.git` out of the build context.
- The base image is referenced by **tag** (`3.14-slim`). Pinning to an exact digest is considered later.

## Consequences

- Dependencies are installed from the lock file, so the image matches what was tested.
- The final image has no uv and no build leftovers, which makes it smaller with less to attack.
- [0005](0005-python-3-14-uv.md) says uv manages Python. Inside the image the base image supplies Python 3.14 instead. The version is the same, the supplier differs.
- Copying `uv.lock` and `pyproject.toml` before the code means a code change does not reinstall every library.
- A `.env` file or other secret can never be baked into an image layer, as long as `.dockerignore` stays correct.
- The slim image has no debugging tools. Tools are added temporarily when needed.
- The uv image comes from Astral's registry, not Docker's official library. Its version is pinned, and a digest check can be added later.
- A tag (`3.14-slim`) brings Python security patches automatically, but the image can change between builds. Digest pinning would make it reproducible at the cost of manual or bot-driven updates.
- A non-root user can cause file-permission surprises if the app starts writing files.
- Uvicorn's first two start-up lines stay plain text until a log configuration is added. That is a separate small step.
- The image is not scanned for known vulnerabilities yet. That is planned for M9.

## What to learn

- Every Dockerfile instruction creates a cached layer. Put what changes rarely first and what changes often last.
- A `.dockerignore` decides what is sent into the build. Without it, secrets can end up in an image permanently.
- A multi-stage build ships the result, not the tools used to make it.
- Running as non-root limits what a bug in the app can do inside the container.
- Inside a container `127.0.0.1` means that container only. The compose file decides what is reachable from the host.
