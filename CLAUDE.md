# Working rules for AI assistants in this repository

Retainly is a public learning project. The author is a senior iOS engineer learning backend, AI engineering and Kotlin Multiplatform. The goal is understanding, not just shipping.

## How to work here (learning first)

For every phase and every new tool or pattern:

1. **Explain first** in plain language: what it is, why it is used, the alternatives and trade-offs.
2. **Agree the decision together**, then record it in `docs/adr/`.
3. **Only then implement**, in small steps, explaining as you go.
4. **End with a recap**: "you are ready when you can explain..." points.

Never adopt a library, pattern or service silently.

## Hard rules

- **Public repository.** Never commit secrets, real contracts, bank statements or personal data. All test data is synthetic. This includes QA material in `qa/` (plans, bug reports, screenshots).
- **Nothing from past employers or clients.** Everything here is original or clearly open source with its licence respected. Do not copy code from AGPL or source-available projects.
- **Money maths is deterministic code.** Amounts are integer minor units plus a currency code. A language model never calculates money.
- **History is never edited.** Contract versions, issued invoices and received payments are append-only.
- **Three kinds of income stay separate:** projected, invoiced, received.
- **Different currencies are never silently added together.**
- **AI output is untrusted until verified.** Quotes from contracts are checked against the source page by code.

## Style

- Plain, simple language in docs and comments. Short sentences.
- Decisions live in `docs/adr/`. The roadmap lives in `docs/ROADMAP.md`.
- Commit only when asked. Do not push.

## Stack (decided)

- Backend: Python, FastAPI, PostgreSQL (`backend/`)
- Shared core: Kotlin Multiplatform (`shared/`)
- iOS: SwiftUI, native screens (`ios/`)
- Android: Jetpack Compose, added in phase M11
- Invoices: UAE only, drafts only, never sent automatically
