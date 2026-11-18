# Security

Retainly is an early-stage learning project. It is not yet running in production and handles no real user data.

## Reporting a vulnerability

Please use GitHub's **private vulnerability reporting** on this repository (Security tab, "Report a vulnerability"). Please do not open a public issue for security problems.

## Ground rules for this repository

- No real contracts, bank statements or personal data are ever committed. Test data is synthetic.
- No secrets are ever committed. `.env` is ignored, and `.env.example` holds placeholders only.
- Secret scanning runs before every commit (pre-commit) and on every push (CI).
