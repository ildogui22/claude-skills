---
name: handoff
description: End-of-session handoff ritual. Invoke before closing a session to persist shared durable knowledge first, then Claude-only memory or plans where appropriate, and flag anything left in-flight. Use when the user says "/handoff", "wrap up", "I'm closing this session", "update memory before I go", or similar end-of-session cues.
---

# Session Handoff

The user opens fresh sessions frequently for cleaner context. This skill is the
ritual run **at the end of a session** so the next one starts fully oriented. The
goal: nothing important lives only in this conversation's context when it closes.

For a project with a knowledge base, invoke `knowledge-maintainer` first. Shared
canonical knowledge is the durable cross-agent record; Claude memory is only
for personal preferences, compatibility context, or material not suitable for a
shared canonical page. Codex has no Claude-memory destination.

**Contract: propose, then write.** Survey the session, present a concise numbered
list of proposed changes, wait for the user's yes (or edits to the list), then apply.
Do not write memory/plan files before that confirmation. (Editing is otherwise
unprompted per the user's accept-edits preference — but persistence to long-term
memory is the one place a quick review gate is wanted, to avoid junk memories.)

## Paths (resolve at runtime — never hardcode a specific project's paths)

- **Memory dir**: the per-project memory directory named in the system prompt's
  memory instructions (e.g. `~/.claude/projects/<slug>/memory/`). Each memory is one
  file; `MEMORY.md` in that dir is the index loaded every session.
- **Plans dir**: `~/.claude/plans/` — plan files from EnterPlanMode/ExitPlanMode.
  The active plan (if any) is usually referenced by a project memory.

## Procedure

### 1. Maintain shared knowledge, then survey personal handoff context
Run the `knowledge-maintainer` knowledge-impact check before proposing memory or
plan changes. Do not duplicate its classification or update workflow here.

Review the conversation for anything the next session would need but can't derive from
the repo, git history, or existing CLAUDE.md/memory:
- **Decisions made** (what and *why* — the why is the part that gets lost).
- **State changes**: what got merged/deployed/pushed, what's now live, env/config flips,
  what a memory previously said is now stale.
- **In-flight work**: what's half-done, the next concrete step, any blockers (and who
  they're blocked on).
- **Corrections/feedback** the user gave on how you should work → these are `feedback` memories.
- **New references**: URLs, PR numbers, tickets, dashboards, secrets-to-rotate.

Skip shared durable facts already captured in canonical knowledge, anything the repo
already records, and anything that only mattered to this conversation. If asked to
remember a shared fact, point to its canonical page instead.

### 2. Reconcile against existing memory
For each candidate, check whether a memory file **already covers it** (grep the memory
dir by topic — don't assume from `MEMORY.md` titles alone). Prefer **updating** the
existing file over creating a near-duplicate. Flag any existing memory this session
**invalidated** — those get edited or deleted, not left to mislead the next session.

### 3. Present the proposal
Show a concise numbered list grouped as **New / Update / Delete / Plan**, one line each:
```
NEW    feedback_x        — <hook>
UPDATE project_v2_rework — mark Phase 6-plumbing engine slice merged; drop stale X line
DELETE project_old_thing — superseded by the merge above
PLAN   i-m-ok-...neumann — check off decisions D2/D5, note session B is next
```
Then ask: **"Apply these? (or tell me what to change)"** Wait for the answer.

### 4. Apply (after yes)
- **Memory files**: match the existing style exactly — frontmatter with `name`,
  `description`, and `metadata` (keep the repo's convention: `node_type: memory`,
  `type: user|feedback|project|reference`, and preserve/set `originSessionId` if present
  on siblings). Body: the fact; for `feedback`/`project` add **Why:** and **How to apply:**
  lines. Link related memories with `[[slug]]` liberally. Convert relative dates to
  absolute (today's date is in the system prompt).
- **MEMORY.md**: add/adjust the one-line pointer (`- [Title](file.md) — hook`) for every
  new/renamed memory. Never put memory content in the index. Remove pointers for deleted files.
- **Plan file**: update status in place — check off completed steps, note what's next, mark
  the plan done if it is. Keep the plan's existing structure.

### 5. Report
End with a 3–5 line summary of exactly what was written/edited/deleted, and — if anything
is left in-flight — a one-line "**Next session, start with:** …" so the handoff is explicit.

## Notes
- Don't `mkdir` the memory dir or check it exists — write directly.
- Never read or print `.env*`/credential files as part of surveying. If a secret leaked
  into this session, record it (which key + where, no value) in the secrets-to-rotate
  reference memory and call it out in the report.
- If the session did nothing worth persisting, say so plainly instead of inventing memories.
