#!/usr/bin/env bash
# Checks that a pull request title follows Conventional Commits.
# See docs/adr/0014-conventional-commits.md.
#
# The title arrives in the PR_TITLE environment variable. It is never pasted
# into a shell command: a pull request title is untrusted input.
set -euo pipefail

title="${PR_TITLE:-}"
max_length=72

types='feat|fix|docs|test|refactor|perf|build|ci|chore|revert|style'
scopes='backend|infra|docs|qa|ios|shared|evals|ci|deps'

# type, optional (scope), optional "!", colon and a space, then a description that
# does not start with a capital letter and does not end with a full stop.
pattern="^(${types})(\((${scopes})\))?!?: [^A-Z[:space:]].*[^.[:space:]]\$"

problems=()

if [[ ! "$title" =~ $pattern ]]; then
  problems+=("The title must look like: type(scope): description")
  problems+=("  types:  ${types//|/, }")
  problems+=("  scopes: ${scopes//|/, } (optional)")
  problems+=("  The description starts with a lowercase letter and has no full stop at the end.")
fi

if (( ${#title} > max_length )); then
  problems+=("The title is ${#title} characters long. The limit is ${max_length}.")
fi

if (( ${#problems[@]} > 0 )); then
  echo "The pull request title does not follow the convention (docs/adr/0014-conventional-commits.md)."
  printf '  got: %s\n' "$title"
  printf '%s\n' "${problems[@]}"
  echo "Examples:"
  echo "  feat(backend): add request-ID logging"
  echo "  fix(infra): publish the database port on localhost only"
  echo "  docs: record the choice of Postgres 18"
  exit 1
fi

printf 'OK: %s\n' "$title"
