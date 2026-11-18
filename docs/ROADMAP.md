# Roadmap

Retainly is built in layers. The deterministic money engine comes first, and AI is added on top of it, so the model never touches the numbers. Every phase ends with something that runs.

Each phase also sits on a rung of an "AI ladder", from no AI at all up to agents.

| Phase | Name | AI stage | Outcome |
|---|---|---|---|
| M0 | Set up the workshop | 0 · Groundwork | Signed-in app talks to a deployed API, and every push is tested and delivered |
| M1 | The money brain | 0 · Groundwork | A tested engine turns a contract's money terms into the correct payment schedule |
| M2 | First screens | 0 · Groundwork | Enter a contract by hand and see a payment calendar and a three-income dashboard |
| M3 | Invoices, payments and a safety net | 0 · Groundwork | Expected payments become invoices and recorded money, with replayable events |
| M4 | Teach the app to read contracts | 1 · Talking to an LLM | Upload a PDF and get terms with their quote and page, graded by tests |
| M5 | When contracts change | 1 · Talking to an LLM | Amendments create new versions without touching history |
| M6 | Ask your contract anything | 2 · Grounded answers (RAG) | Cited answers from the right contract |
| M7 | AI that stays on your phone | 3 · AI on your phone | Private content handled on-device, with proof of what leaves it |
| M8 | Bank statements and who paid what | 4 · AI over numbers | Statement import, deposit matching and on-device expense sorting |
| M9 | Make it tough, then ship it | 5 · AI in the real world | Load tests, monitoring, drills and the first App Store release. Optional drill: a security responder for leaked-secret alerts |
| M10 | The billing helper | 6 · Agents and MCP | An agent prepares billing for approval, plus a read-only MCP server |
| M11 | The Android app | 7 · AI on a second platform | Android on the same shared Kotlin core |

## Scope decisions

- Native screens on both platforms. Compose Multiplatform is not planned.
- A wide shared Kotlin core: models, networking, storage, validation, parsing.
- Invoices cover the UAE only, as drafts. Nothing is ever sent automatically.
- FastAPI and PostgreSQL for the backend.

Decisions and their reasoning live in [`adr/`](adr/).
