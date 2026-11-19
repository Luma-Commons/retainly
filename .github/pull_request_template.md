## What this changes

Say what changed and why, in plain language.

The pull request **title** becomes the commit message on `main`. Use the format `type(scope): description`, for example `feat(backend): add request-ID logging`. See [CONTRIBUTING.md](../CONTRIBUTING.md).

## How it was checked

- [ ] I ran the checks that apply (for backend changes: `uv run ruff check .`, `uv run ruff format --check .`, `uv run pyright`, `uv run pytest` from `backend/`)
- [ ] For documents (QA plans, ADRs): I re-read them and the links work

## Safety

- [ ] No secrets, real contracts, bank details or personal data, including in screenshots
- [ ] Any new test data is synthetic

## Decisions

- [ ] If this adopts a new library, tool or pattern, there is a decision record in `docs/adr/`
