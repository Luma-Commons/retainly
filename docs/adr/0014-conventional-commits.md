# 0014. Conventional Commits and squash merging

- **Status:** Accepted
- **Date:** 2026-11-19

## Context

`main` is protected ([0011](0011-qa-folder-and-collaboration.md)), so every change arrives through a pull request. Two people will work in the repository, and one of them mostly edits documents on the GitHub website. We want a history that is easy to scan, and a rule that is simple enough to enforce for everyone.

The first three commits on `main` have free-form messages. `main` is protected public history, so they are not rewritten.

## Options considered

**Message format**

1. **Free-form messages.** No rule, no effort. History varies from commit to commit.
2. **Conventional Commits 1.0.0.** `type(scope): description`, with types such as `feat`, `fix` and `chore`. An open standard that many teams and tools understand.
3. **Ticket-ID prefixes.** Useful with an issue tracker, but this project has no ticket system.

**Merge strategy**

1. **Squash merge.** One commit per pull request on `main`, titled with the pull request title. Only the title needs to follow the rule.
2. **Merge commit or rebase.** Every commit on the branch lands on `main`, so every message needs to follow the rule.

## Decision

- **Conventional Commits 1.0.0.** The format is `type(scope): description`, with `!` before the colon for a breaking change.
- **Types:** `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`, `revert`, and `style` (rarely, because ruff formats code).
- **Scopes (optional):** `backend`, `infra`, `docs`, `qa`, `ios`, `shared`, `evals`, `ci`, `deps`.
- **Style:** imperative mood, no capital letter after the colon, no full stop at the end, the whole title at most 72 characters.
- **Squash merge only.** The squashed commit takes the **pull request title** as its title.
- A **CI check on the pull request title**, written as a small script in this repository with no third-party action, and made a **required check** on `main`.
- Commits on a branch are free-form, because squash merging replaces them with the title. A clear message is still encouraged.
- Existing commits on `main` stay as they are. The convention starts with the first pull request after this record.
- Choosing between types is a judgement call. Pick the closest one and move on.

## Consequences

- `git log` on `main` reads like a changelog, and release notes can be generated from it later.
- There is one rule to enforce: the title. This suits a collaborator who edits on the website and never runs `git commit`.
- Fine-grained commits from a branch are not kept on `main`. They remain visible in the closed pull request.
- The title is untrusted input, so the check passes it to the script through an environment variable and never writes it into the shell command itself. Otherwise a crafted title could run commands in CI.
- Whether a change is a `feat`, a `build` or a `chore` is subjective, so some titles will be debatable.
- The first three commits on `main` do not follow the format, and stay that way.
- The check only runs on pull requests. A direct push to `main` is already blocked by the branch rules.
- No local `commit-msg` hook for now. It would help only on one machine, and the title is what counts.

## What to learn

- A conventional message has three parts: a type, an optional scope and a short description.
- With squash merging, the pull request title becomes the commit message on `main`.
- Text from a pull request (title, branch name, description) is untrusted input in a workflow.
- A rule that can be enforced for everyone in one place is more likely to be followed.
