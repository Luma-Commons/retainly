# 0011. QA folder and collaboration rules

- **Status:** Accepted
- **Date:** 2026-11-18

## Context

A QA collaborator is joining the project. She will mostly write test plans and checklists, test the product and report bugs. The repository is public, and decision [0001](0001-monorepo.md) keeps everything in one repository. We need to say where QA work lives, how bugs are reported, and how changes reach `main` safely when two people work in it.

## Options considered

**Where QA work lives**

1. **A `qa/` folder in this repository.** One place for code, tests and QA documents. History and reviews stay together.
2. **A separate QA repository.** Cleaner separation, but it splits the history and breaks the reasoning of ADR 0001.
3. **QA documents inside `docs/`.** Fewer folders, but QA material is mostly working documents, not architecture, and it would get mixed in with the decisions.

**How she gets access**

1. **Write role on a protected `main`.** She works on branches and opens pull requests.
2. **Fork and pull request only.** The safest, but awkward for someone who mostly edits documents.
3. **Admin role.** Full control, including settings and deleting the repository. More than she needs.

## Decision

- QA documents live in **`qa/`**: test plans in `qa/test-plans/`, manual checklists in `qa/checklists/`.
- **Bugs are reported as GitHub Issues** using a bug template. A bug report asks for the request ID (the `X-Request-ID` header from [0010](0010-structlog-request-ids.md)), so a developer can find the exact request in the logs.
- **Automated tests stay next to the code they test** (for example `backend/tests/`). QA can add to them through pull requests.
- **AI evals stay in `evals/`.** They grade AI features. QA tests the product.
- The collaborator has the **Write role**, as an **outside collaborator on this repository only**, not as a member of the hosting organisation. Organisation members can read the organisation's private repositories by default, and she has no need to.
- `main` is protected: changes arrive only through pull requests, the secret-scan check must pass, and force-pushes and deletion are blocked.
- Required approvals are **0 for now**, because GitHub does not let an author approve their own pull request, and there is no second code reviewer yet. This is raised to 1 when there is one.
- **The same hard rules apply to QA material:** synthetic data only, no secrets, no real contracts, statements or personal data, including in screenshots and bug reports.

## Consequences

- QA work is reviewed and versioned like code.
- Bug reports that carry a request ID connect directly to the logs.
- Anyone with Write access can create branches in the repository, so branch protection and the secret-scan check are the safety net, not trust alone.
- With 0 required approvals, a mistake can be merged by its own author once the checks pass. We accept this for a two-person learning project and revisit it.
- A public issue tracker means bug reports are public. The template tells reporters not to paste real data or secrets.
- Until CI runs ruff, pyright and pytest (a later step), only the secret-scan check is enforced on pull requests.

## What to learn

- A protected branch cannot be changed directly. Every change goes through a pull request.
- A pull request is a proposed change that others can review and that automated checks can test before it is merged.
- A collaborator's role decides what she can do. Give the least that works.
- Documents about testing and automated tests have different homes: documents in `qa/`, tests beside the code.
