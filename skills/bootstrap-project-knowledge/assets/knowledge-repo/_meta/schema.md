# Schema and truth model

Change this schema conservatively: churn makes future retrieval less predictable.

## Core model

| Type | Question answered | Directory |
|---|---|---|
| `concept` | What does this mean? | `domain/` |
| `system` | How do these parts work together? | `systems/` |
| `decision` | What was chosen, and why? | `decisions/` |
| `initiative` | What is the current delivery state? | `initiatives/` |
| `question` | What remains unresolved? | `questions/` |
| `source` | What original evidence is available? | `sources/records/` |

A page has one primary type. When a subject needs both stable explanation and
fast-moving status, use a system page plus a linked initiative page.

## Required frontmatter

Every canonical content page starts with:

```yaml
---
title: Human-readable title
type: concept
status: draft
updated: YYYY-MM-DD
scope: []
sources: []
related: []
---
```

Use quoted path-form wikilinks in `sources` and `related`, without `.md`:
`- "[[domain/example]]"`. Use path-form wikilinks in prose as well, optionally
with an alias: `[[domain/example|example]]`. `index.md`, `sources/index.md`,
README files, and `_meta/` use ordinary Markdown links for Git-host rendering.

## Lifecycle values

- Concepts and systems: `draft`, `synthesized`, `accepted`, `verified`, `superseded`
- Decisions: `proposed`, `accepted`, `superseded`
- Initiatives: `planned`, `active`, `blocked`, `complete`, `cancelled`
- Questions: `open`, `answered`, `deferred`
- Sources: `current`, `superseded`, `unavailable`

Only the user or an authoritative project record can make a decision `accepted`.
Agent-derived conclusions remain `synthesized` until accepted. Use `verified`
only for claims recently checked against the appropriate primary evidence.

## Contextual authority

| Claim | Prefer |
|---|---|
| What is live now? | Runtime evidence, then active configuration |
| What is implemented? | Current code, migrations, and tests |
| What was intentionally chosen? | Accepted decision, then approved plan |
| What work is current? | Git, issue, deployment, or delivery evidence |
| What does an external rule say? | Current official primary source |
| Why is it interpreted this way? | Accepted rationale plus cited evidence |

Plans, conversations, old memory, and wiki prose may guide discovery but do not
prove current implementation or external facts. When sources conflict, preserve
both claims, verify against the appropriate authority, and leave an open question
if the conflict remains.

## Canonical and temporal rules

- Give one subject one canonical page.
- Prefer pages that answer reusable questions, not one page per session or source.
- Split subjects whose sections have different authorities or lifecycles.
- Put current state, next step, and blockers near the top of initiatives.
- Replace stale state instead of appending dated status entries.
- Keep decision-relevant history only when it explains the present.
- Give volatile claims a `Last verified` line with the evidence checked.
- Omit superseded pages from active indexes and move them to `archive/` when useful.

## Sources and secrets

A source record identifies and evaluates an original source. Preserve a local
artifact only when offline access, immutability, or reproducibility justifies it.
Record location, retrieval parameters, date, and checksum for large artifacts.

Never store secrets, credentials, tokens, recovery codes, `.env*` contents,
private keys, service-account files, or credential-bearing URLs.

## Index contract

`index.md` lists every active non-source page once, grouped by type and followed
by a one-sentence description. `sources/index.md` lists every active source once.
`_meta/log.md` records material operations and replaces neither index.
