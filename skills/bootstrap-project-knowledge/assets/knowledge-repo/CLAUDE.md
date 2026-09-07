# {{PROJECT_NAME}} knowledge base

This repository is the persistent knowledge layer for Claude Code and Codex.
`AGENTS.md` is a symlink to this file so both agents receive the same rules.

## Required workflow

For every task in this repository:

1. Read `index.md` first.
2. Search for an existing canonical page before creating one.
3. Read `_meta/schema.md` before changing page structure or metadata.
4. Follow `_meta/workflows.md` for retrieval, ingest, updates, and linting.
5. Verify volatile or implementation claims against primary evidence.
6. Perform the knowledge-impact check before finishing.
7. Add an `_meta/log.md` entry only for a material knowledge change.

Run `make lint` after changing the knowledge base.

## Knowledge rules

- Give each durable subject one canonical home; link instead of duplicating.
- Present current truth first and preserve uncertainty.
- Distinguish observation, accepted decision, agent synthesis, and unknowns.
- Treat plans and conversations as evidence of intent, not implementation.
- Use Git history plus `_meta/log.md` for chronology instead of status diaries.
- Never read, copy, summarize, or store `.env*`, credentials, tokens, recovery
  codes, service-account files, credential-bearing URLs, or candid private notes.
- Migrate existing material one topic at a time; never bulk-dump old context.

## Repository map

- `domain/` — durable terminology and concepts
- `systems/` — relationships, flows, and cross-component behavior
- `decisions/` — accepted, proposed, and superseded choices
- `initiatives/` — current delivery state, blocker, and next step
- `questions/` — genuine unresolved or deferred issues
- `sources/records/` — provenance and authority records
- `sources/artifacts/` — preserved immutable source copies when justified
- `archive/` — superseded material outside the active surface
- `_meta/` — schema, workflows, templates, and maintenance log

## Git

This is an independent repository. Follow the user's applicable Git workflow.
Do not commit or push merely because knowledge files changed unless a project or
user instruction explicitly authorizes that behavior.
