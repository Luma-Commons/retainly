# Image for the Retainly API. See docs/adr/0013-api-container-image.md.
#
# Build (from the repo root):  docker build -t retainly-api:dev backend
#
# Two stages: the first installs the libraries, the second copies only the result.

# ---- Stage 1: builder (has uv, installs the libraries) ----------------------
FROM python:3.14-slim AS builder

# uv is pinned to the version we use locally. Upgrade both together.
COPY --from=ghcr.io/astral-sh/uv:0.13.0 /uv /bin/uv

# COMPILE_BYTECODE: faster start-up. LINK_MODE=copy: a plain copy of the files,
# so the folder can be moved to the next stage. PYTHON_DOWNLOADS=never: use the
# Python from the base image, and do not let uv download its own.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Copy only the two files that describe the libraries. Docker reuses this layer
# until they change, so a change to our own code does not reinstall everything.
COPY pyproject.toml uv.lock ./

# --locked: fail if uv.lock does not match pyproject.toml (exact versions).
# --no-dev: leave out ruff, pyright and pytest.
# --no-install-project: install the libraries only, our code is copied later.
RUN uv sync --locked --no-dev --no-install-project

# ---- Stage 2: final image (no uv, no build leftovers) -----------------------
FROM python:3.14-slim

# An ordinary user, so a bug in the app cannot act as the container's administrator.
RUN useradd --system --create-home --uid 10001 app

WORKDIR /app

# Only the finished libraries from stage 1, then our code (which changes often).
# Both stay owned by root and read-only to the app user.
COPY --from=builder /app/.venv /app/.venv
COPY app ./app

# Put the libraries' programs (uvicorn) first on the path.
# UNBUFFERED: log lines appear at once instead of waiting in a buffer.
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER app

# Documentation only: the app listens on this port. Compose decides what is published.
EXPOSE 8000

# Ask our own GET /health route. The slim image has no curl, so we use Python.
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import sys, urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).status == 200 else 1)"]

# 0.0.0.0 means "all addresses INSIDE the container", so that it can be reached from
# outside. The compose file decides what is reachable from your Mac.
# --log-config makes Uvicorn's own first lines use our log format.
# --no-access-log: our middleware writes one summary line per request instead.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--log-config", "app/uvicorn_logging.json", "--no-access-log"]
