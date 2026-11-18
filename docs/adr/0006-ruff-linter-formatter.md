# 0006. Ruff for linting and formatting

- **Status:** Accepted
- **Date:** 2026-11-16

## Context

Python has no compile step, so many mistakes (unused code, misspelled names, risky patterns) only show up when a line runs. A linter finds them early. A formatter keeps the layout of the code the same everywhere.

Most code here is written by an AI assistant. Style drifts between sessions, and AI code can look confident while containing small mistakes. The author reviews the code and is also learning Python, so consistent, checked code matters more, not less.

## Options considered

1. **flake8 + black + isort.** The classic set. Three tools and three configs, and flake8 needs plugins for most checks.
2. **pylint.** Deep and strict, but slow and noisy.
3. **Ruff.** Linter, formatter and import sorter in one tool, with one config in `pyproject.toml`. Very fast. Made by Astral, who also make uv.

## Decision

- **Ruff** for linting, formatting and import sorting.
- Config in `pyproject.toml`. First rule groups: `E` and `F` (basic errors, unused code), `I` (import order), `B` (likely bugs), `UP` (modern Python syntax). More groups are added when each is understood.
- Runs in **pre-commit** and in **CI**. CI is the one that enforces the rules.
- The AI assistant runs it after every change.
- Editor integration is optional and is not part of this decision.

## Consequences

- One tool and one config replace several.
- Every pull request has the same style, so diffs show real changes.
- Mistakes common in AI-written code (unused imports, bare `except`, mutable default arguments) are caught automatically.
- Ruff's formatter follows black's style but is not identical in every case.
- Turning on all rules would be noisy, so we add rule groups step by step.
- Pylint catches some deeper problems that ruff does not. A type checker (next decision) covers much of that gap.
- Ruff and uv both come from Astral. Both are open source, but it is a small concentration of tooling in one company.

## What to learn

- A formatter changes layout only. A linter reports likely mistakes, and can fix some of them.
- Python needs a linter more than Swift does, because there is no compiler to catch errors before the code runs.
- Checks that run automatically (pre-commit, CI) matter more than checks that depend on someone remembering to run them.
- Linting is a cheap check on AI-written code, in line with "AI output is untrusted until verified".
