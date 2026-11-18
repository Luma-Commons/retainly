# Retainly

**Upload a contract. See your income. Stay on top of invoicing.**

Retainly is an app for independent contractors. You upload an agreement once. The app reads its commercial terms, builds a calendar of the payments you should expect, forecasts your income, drafts invoices and answers questions about the contract, with every answer tied to a quote from the document.

> **Status: early stage.** Phase M0 (project foundation) is in progress. Nothing here is production software yet.

## Why this exists

This is a **learning project, built in public**. The author is a senior iOS engineer using it to learn backend engineering, AI engineering and Kotlin Multiplatform properly, by building something real. Every technical choice is explained and recorded in [`docs/adr/`](docs/adr/), so the reasoning is visible as well as the code.

## The one idea to remember: three kinds of income

| | Meaning |
|---|---|
| **Projected** | What the contract says you should earn. A forecast |
| **Invoiced** | What you have asked clients to pay |
| **Received** | What has actually landed in your bank |

The app keeps these apart on every screen and never blends them.

## Principles

- Expected payments are the central entity. Invoices follow from them.
- Money is calculated by deterministic code. A language model never does the maths.
- Every fact taken from a contract comes with its quote and page, checked by code.
- You review and confirm before anything counts.
- History is never rewritten. A change creates a new version with a start date.
- Different currencies are never silently added together.

## Architecture (planned)

```
iOS app (SwiftUI)   Android app (Compose, later)
        \               /
     Shared Kotlin core (models, networking, storage)
                  |
        FastAPI backend  ---  PostgreSQL
                  |
        Claude API (contract reading, cited answers)
```

Screens are native on each platform. Only logic is shared.

## Repository layout

| Folder | What lives there |
|---|---|
| [`backend/`](backend/) | Python FastAPI service, database migrations, tests |
| [`shared/`](shared/) | Kotlin Multiplatform core shared by iOS and Android |
| [`ios/`](ios/) | The SwiftUI app |
| [`infra/`](infra/) | Docker and deployment setup |
| [`fixtures/`](fixtures/) | Golden test cases that the server and the Kotlin core must both pass |
| [`evals/`](evals/) | Test set and graders for the AI features (synthetic data only) |
| [`qa/`](qa/) | Manual test plans and checklists. Bugs are tracked as GitHub Issues |
| [`docs/`](docs/) | Roadmap and architecture decision records |

Want to help? See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Roadmap

See [`docs/ROADMAP.md`](docs/ROADMAP.md). It is built in layers: a tested money engine first, then AI on top of it.

## How AI tools are used here

The project is built with Claude Code as a teaching and pairing tool. The author reviews and understands every change, and AI output is treated as untrusted until verified. Working rules for AI assistants are in [`CLAUDE.md`](CLAUDE.md).

## Not advice

Retainly is a record-keeping tool. It does not give legal, tax or financial advice. Answers about contracts quote the document and are not legal interpretation.

## Data

All sample data in this repository is synthetic. No real contracts, statements or personal data are committed.

## Licence

Apache-2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE). The licence covers the code, not the name or logo.
