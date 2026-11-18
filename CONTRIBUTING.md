# Contributing

Retainly is a public learning project with a small team. This page explains how changes reach `main`.

## The short version

1. **Never push straight to `main`.** It is protected.
2. Make a **branch**, change what you need, and open a **pull request**.
3. Wait for the automated checks to pass, then merge.

## Step by step

1. Create a branch from `main` with a short name, for example `qa/health-check-plan`.
2. Make your change. Keep it small and about one thing.
3. Commit with a clear message that says what changed and why.
4. Push the branch and open a pull request. Fill in the template.
5. The **secret scan** runs automatically. It must pass.
6. Merge when it is green. If a change touches someone else's area, ask them to look first.

Editing a file directly on the GitHub website also works for documents. GitHub creates the branch and the pull request for you.

## Who looks after what

| Area | Who |
|---|---|
| `qa/` (test plans, checklists) | The QA collaborator |
| Everything else (code, decisions, roadmap) | The project author |

Anyone can open an issue or suggest a change anywhere.

## Rules that apply to everyone

- **This repository is public.** Never commit secrets (API keys, passwords, tokens) or real data (contracts, bank statements, personal details). Test data is always synthetic. This includes screenshots and bug reports.
- **Nothing from an employer or client.** Everything here is original or open source with its licence respected.
- **New tools and patterns need a decision record** in [`docs/adr/`](docs/adr/) before they are adopted.
- **Plain language.** Short sentences in documents and comments.

## Reporting bugs

Open an issue and choose **Bug report**. If the problem came from the API, include the `X-Request-ID` from the response headers. Security problems are different: follow [`SECURITY.md`](SECURITY.md) and do not open a public issue.
