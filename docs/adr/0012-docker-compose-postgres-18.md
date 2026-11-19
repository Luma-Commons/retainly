# 0012. Docker Compose with PostgreSQL 18 for local development

- **Status:** Accepted
- **Date:** 2026-11-19

## Context

The backend needs a PostgreSQL database ([0004](0004-python-fastapi-backend.md)). The author, a QA collaborator and CI all need to run the same setup without installing and tuning things by hand. Differences in versions between machines cause bugs that appear on one machine and not another.

## Options considered

PostgreSQL versions were checked on 2026-11-19. 18 is the current major version (18.7, supported until November 2030). 17 is supported until 2029. 14 reached its end of life in November 2026.

1. **Postgres installed with Homebrew on each Mac.** Quick, but versions drift and it cannot be handed to a QA collaborator or CI.
2. **Docker Compose with the official Postgres image.** The same version for everyone, disposable, started with one command.
3. **A hosted development database (for example Neon or Supabase).** Needs accounts and internet, and risks real data ending up in a shared place.
4. **SQLite for development and Postgres for production.** Behaviour differs between the two, which hides bugs.

## Decision

- **Docker Compose** for local development, with **PostgreSQL 18** from the official image, pinned to the **major version**.
- A **Dockerfile** for the API in `backend/`: Python 3.14 slim base, uv with the committed lock file, a non-root user, and a health check that calls `GET /health`.
- A **compose file** that describes the API container, the database container, the volume, the ports and the environment.
- The database has a **volume**, so data survives the container being removed.
- The database port is published on **127.0.0.1 only**, so only the local machine can reach it.
- Passwords in compose files are **throwaway development values**. They are never reused anywhere real, and real secrets never go in these files.
- The container engine (OrbStack, Docker Desktop, Colima) is each person's **local choice**. The files work with any of them.
- Inside the compose network the API reaches the database by its service name (for example `db`), not `localhost`. The setting comes from the environment ([0009](0009-pydantic-settings-configuration.md)).

## Consequences

- Everyone, including CI, runs the same database version.
- A new person starts the whole stack with one command.
- A container engine must be installed and running.
- Docker uses memory and disk.
- Volumes can confuse newcomers: deleting the volume deletes the data.
- Pinning only the major version still lets minor releases arrive, which is intended for security fixes. We move to a new major version deliberately, with a new decision record.
- At the time of writing, Postgres 18's official image is believed to store its data in a different place from earlier versions, so the volume path must be checked against the image documentation when the compose file is written.
- This decision does not choose how Python talks to the database, or how the schema changes over time. Those are separate decisions.

## What to learn

- An image is a read-only package. A container is a running copy of it, and containers are disposable.
- A Dockerfile builds one image. A compose file runs several containers together.
- A database container needs a volume, or its data disappears with it.
- `localhost` inside a container means that container itself.
- Pin versions that can change behaviour, and bind services to localhost unless they must be reachable.
