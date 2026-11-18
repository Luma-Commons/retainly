# 0003. Public from day one, with safeguards

- **Status:** Accepted
- **Date:** 2026-11-14

## Context

The project is a learning project, and its repository is meant to be seen by hiring managers. It could be developed privately and opened later, or be public from the first commit.

## Options considered

1. **Private first, public later.** Early mistakes stay hidden. The learning journey and the full history are not visible, and a later switch needs care so nothing sensitive is exposed.
2. **Public from day one.** Shows the whole journey and the reasoning. Anything committed is visible, and git history is permanent.

## Decision

Public from day one, with safeguards in place before the first commit.

## Safeguards

- `.gitignore` covers secrets, environment files, keys, local data and build output.
- `.env.example` holds placeholders only. Real values live in `.env`, which is ignored.
- Secret scanning runs before every commit (pre-commit with gitleaks) and on every push (CI).
- GitHub push protection and secret scanning are enabled on the repository.
- All sample data is synthetic. No real contracts, statements or personal data are committed.
- If a secret is ever committed, the key is rotated immediately. Deleting the file is not enough, because history keeps it.

## Consequences

- Hiring managers can read the commit history, the decision records and the tests.
- Early commits are visible, so messages and structure should be tidy from the start.
- Production configuration and keys are kept out of the repository entirely.

## What to learn

- Git history is permanent. A secret removed in a later commit is still in the earlier ones.
- The fix for a leaked secret is to rotate it, not to hide it.
- Preventing a leak (scan before commit) is far cheaper than cleaning up after one.
