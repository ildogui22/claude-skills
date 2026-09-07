# Cross-agent parent routing

Add the following material to the parent workspace's `CLAUDE.md`. Adapt the
placeholders and preserve stronger project-specific instructions.

```markdown
## Project knowledge

The canonical project knowledge base is `<KNOWLEDGE_DIR>/`, an independent Git
repository inside this workspace.

For every substantive project task:

1. Use the `knowledge-maintainer` skill when it is available.
2. Read `<KNOWLEDGE_DIR>/index.md` first and retrieve only the smallest relevant
   set of canonical pages.
3. Treat the knowledge base as maintained synthesis. Verify volatile status,
   implementation, and external claims against the appropriate primary evidence.
4. Before finishing, perform the knowledge-impact check in
   `<KNOWLEDGE_DIR>/_meta/workflows.md`; update the canonical page only when the
   task materially changed durable knowledge.
5. Never store secrets, `.env*` contents, credential-bearing URLs, or private
   candid notes in the knowledge repository.

Before modifying a child repository, read that repository's `CLAUDE.md` or
`AGENTS.md`. The parent router does not replace child-repository instructions.
```

## Child-repository block

Add this compact block to each child repository's `CLAUDE.md`. Calculate the
path relative to that repository; a common sibling layout uses
`../<KNOWLEDGE_DIR>`.

```markdown
## Shared project knowledge

The canonical cross-project knowledge base is `<RELATIVE_KNOWLEDGE_DIR>/`.
For substantive work, read `<RELATIVE_KNOWLEDGE_DIR>/index.md` first, retrieve
narrowly, verify volatile claims against primary evidence, and perform the
knowledge-impact check in `<RELATIVE_KNOWLEDGE_DIR>/_meta/workflows.md` before
finishing. Use the `knowledge-maintainer` skill when available. Never store
secrets, `.env*` contents, or candid private notes there.
```

## File topology

Prefer one source of truth:

```text
parent/
├── CLAUDE.md
├── AGENTS.md -> CLAUDE.md
├── code-repository/
└── <project>_knowledge/
    ├── CLAUDE.md
    ├── AGENTS.md -> CLAUDE.md
    ├── index.md
    ├── domain/
    ├── systems/
    ├── decisions/
    ├── initiatives/
    ├── questions/
    ├── sources/
    ├── archive/
    └── _meta/
```

Claude Code natively discovers personal skills in `~/.claude/skills/`. Codex
natively discovers personal skills in `~/.agents/skills/`. A canonical skill in
one location plus a relative directory symlink in the other prevents drift.

The `AGENTS.md -> CLAUDE.md` symlink gives both agents the same project rules.
Commit that symlink inside each Git repository; an untracked local symlink will
disappear from clones and worktrees.

## Verification prompts

Start a fresh session from the parent workspace and ask each agent:

```text
Which project instruction files and knowledge entry point apply here?
```

Then start a fresh session inside a child repository and ask the same question.
Confirm that the child instructions include the compact knowledge route and that
its relative path reaches the same index used from the parent workspace.
