# 0002. Apache-2.0 licence

- **Status:** Accepted
- **Date:** 2026-11-14

## Context

The repository is public. Without a licence, nobody has permission to reuse the code. The code will also ship in an iOS app on the App Store, which limits the licences we can use.

## Options considered

1. **MIT.** Very short and permissive. No patent grant and nothing about names.
2. **Apache-2.0.** Permissive like MIT, plus an explicit patent grant, and it states that it gives no rights to use the project's name or trademarks.
3. **GPL or AGPL.** Anyone who uses the code must open-source their own. GPL has a long-known conflict with Apple's App Store terms, and some employers avoid it.

## Decision

Apache-2.0, with a `NOTICE` file.

## Consequences

- The code is free to use, change and redistribute, with attribution.
- The name "Retainly" and any logo are not licensed for others to use.
- We must respect other projects' licences. We use Firefly III (AGPL) and Actual Budget (MIT) only as references for ideas, and never copy code from AGPL or source-available projects into this repository.
- Every dependency we add must have a licence compatible with Apache-2.0 and App Store distribution.

## Addendum (2026-11-18): repository host and copyright holder

The repository is hosted in the GitHub organisation **Luma-Commons**. The copyright holder named in `NOTICE` is **"Nikhil Nangia and Luma Commons"**. The licence itself is unchanged: Apache-2.0. GitHub's starter file in the new repository used MIT with Luma Commons as holder. It was replaced by this licence, because MIT and Apache-2.0 cannot both apply to the same code.

## What to learn

- A licence defines what others may do with your code.
- "Permissive" licences (MIT, Apache-2.0) allow commercial reuse. "Copyleft" licences (GPL, AGPL) require derived work to be open too.
- Reading how a project works is fine. Copying its code is governed by its licence.
