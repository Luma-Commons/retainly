# 0001. One monorepo

- **Status:** Accepted
- **Date:** 2026-11-14

## Context

Retainly has several parts: a Python backend, a Kotlin shared core, an iOS app, later an Android app, plus docs and infrastructure. They could live in one repository or in several.

## Options considered

1. **Polyrepo** (`retainly-backend`, `retainly-ios`, `retainly-core`, and so on).
   Each part has its own history, permissions and release schedule. This suits large teams. A change that touches both server and app needs several pull requests merged in the right order, and shared test data must be copied, which lets it drift.
2. **Monorepo** (one repository, one folder per part).
   One change can update the API and its clients together, there is one CI setup, and shared test data lives in one place. The repository grows over time, and everyone sees everything.

## Decision

One public monorepo, `retainly`.

## Consequences

- Golden test cases in `fixtures/` are read by both the backend and the Kotlin core, so they cannot drift apart.
- A visitor sees the whole system in one place, with one README.
- CI jobs run only for the folders that changed (path filters).
- Production configuration and secrets never live in the repository.
- **Planned exception:** the MCP server (phase M10) gets its own small public repository, `retainly-mcp`, because it is a focused piece that is useful on its own.
- We would split the repository if collaborators needed access to only one part, if one piece should be open-sourced separately, or if a part needed a different release rhythm.

## What to learn

- Monorepo and polyrepo trade coordination cost against separation.
- For one developer, coordination cost dominates, so a monorepo wins.
- Splitting a monorepo later is possible with history-rewriting tools. Merging separate repositories is harder, so starting together keeps both options open.
