# 0004. Python and FastAPI for the backend

- **Status:** Accepted
- **Date:** 2026-11-16

## Context

Retainly needs a server that stores data, runs the money engine, reads contracts with a language model and keeps secrets (such as API keys) out of the mobile apps. One of the project's goals is for the author to learn backend and AI engineering.

## Options considered

1. **FastAPI (Python).** Typed request and response models (Pydantic), automatic OpenAPI documentation, built around `async`. Small and explicit. Python is where the AI libraries live. Not batteries-included, so we choose the database layer, migrations, login and background jobs ourselves.
2. **Django (Python).** Everything included (ORM, admin, login). More hidden behaviour to learn and heavier for a small API.
3. **Flask (Python).** Very simple, but sync-first, and validation and docs are add-ons.
4. **NestJS (TypeScript).** Strong typing and a large job market, but separates the backend from the Python AI ecosystem.
5. **Rails (Ruby).** Mature and productive, but a different ecosystem from the AI libraries.
6. **Vapor (Swift).** Same language as the iOS app, but a small ecosystem and job market, with few AI libraries.

## Decision

Python with FastAPI, on PostgreSQL.

## Consequences

- Pydantic models describe and validate every input and output at the edge of the service.
- FastAPI generates an OpenAPI description of the API, which later feeds the Kotlin shared core (decided in a later record).
- `async` fits calls to Claude, which wait on the network.
- We must make our own choices for the database layer, migrations, login and background jobs. Each gets its own decision record when we reach it.
- We must avoid running slow blocking code inside `async` routes, because it stalls the whole server.
- Python checks types only at the edges (Pydantic). A static type checker is added later to cover the rest.

## What to learn

- A backend keeps secrets, runs shared logic and stores data that a phone cannot.
- Pydantic models play the role that `Codable` structs play in Swift, with built-in value checks.
- OpenAPI is a machine-readable description of an API, so tools can generate documentation and client code from it.
- `async` lets one server handle many waiting requests at once.
