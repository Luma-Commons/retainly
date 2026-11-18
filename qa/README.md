# qa

Everything about **testing the product by hand and finding problems**: test plans, checklists and the process for reporting bugs.

Automated tests are not here. They live next to the code they test (for example `backend/tests/`). AI grading lives in [`evals/`](../evals/).

## What lives where

| Place | What it holds |
|---|---|
| [`test-plans/`](test-plans/) | One plan per feature or phase: what to test, with which data, and what should happen |
| [`checklists/`](checklists/) | Short manual checks to repeat, such as a smoke test before a release |
| GitHub **Issues** | Every bug, using the bug template. Bugs are not stored as files here |

## How to report a bug

1. Open a new issue and choose **Bug report**.
2. Say what you did, what you expected and what happened.
3. If the problem came from the API, copy the **`X-Request-ID`** value from the response headers. It is a random label for that one request. A developer uses it to find every log line from that request.
4. Never paste real data or secrets (see below).

## How to write a test plan

1. Copy [`test-plans/0000-template.md`](test-plans/0000-template.md) to a new file, for example `0001-health-check.md`.
2. Fill it in. Keep cases short, with one expected result each.
3. Record the result of each case when you run it, and the date.
4. Open a pull request. Never push directly to `main`.

## The rules that apply here too

- **Synthetic data only.** Test contracts, names, amounts and bank details must be made up. Never use a real contract, statement or personal detail, not even in a screenshot.
- **No secrets.** No API keys, passwords or tokens in a plan, a bug report or an attachment.
- **Plain language.** Short sentences. Say what you saw, not what you think the cause is.

## What can be tested today

Right now the project has one API route, `GET /health`, and its generated documentation page. Running the backend on your own machine becomes simple once the Docker step is done (see the [roadmap](../docs/ROADMAP.md)). Until then, test plans and checklists can be prepared in advance for the phases that come next.
