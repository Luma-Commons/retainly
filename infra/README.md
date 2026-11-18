# infra

Docker and deployment setup: generic, reusable configuration only.

**Rule:** real environment values, keys and production settings never live in this repository. They belong in GitHub Actions secrets and the cloud provider's secret store.

**Starts in:** M0 (local Docker). Cloud deployment arrives in M0 and M9.
