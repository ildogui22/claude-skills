---
name: bootstrap-project-knowledge
description: Bootstrap a separate, agent-maintained knowledge repository inside a project workspace. Use when the user wants shared durable project knowledge, a Karpathy-style knowledge layer, or cross-agent context that works across Claude Code and Codex; use when another skill has established that a substantial project needs this knowledge infrastructure.
---

# Bootstrap Project Knowledge

Create an index-first knowledge repository that compiles durable project truth
without replacing code, tests, plans, instructions, or original evidence.

## 1. Resolve the workspace

Identify the parent workspace, its project or product repositories, and a short
project slug. Default the knowledge repository to `<slug>_knowledge/` beside the
code repositories, inside the parent workspace. Treat it as an independent Git
repository even when the parent workspace is itself a repository.

Inspect existing `CLAUDE.md`, `AGENTS.md`, `.gitignore`, and knowledge folders.
Preserve existing instructions and user changes. If a non-empty target already
exists, audit and repair it against the scaffold instead of overwriting it.

Completion criterion: the parent, target, and collision behavior are known.

## 2. Create the knowledge repository

Run the bundled bootstrapper from this skill directory:

```bash
uv run scripts/bootstrap_project_knowledge.py \
  /absolute/path/to/parent \
  --project-name "Human project name"
```

Pass `--knowledge-name name_knowledge` only when the inferred directory name is
wrong. Pass `--no-git` only when the user explicitly declines an independent
Git repository. The script refuses to overwrite a non-empty target.

Completion criterion: the target contains the six canonical page directories,
source records, schema, workflows, templates, linting scripts, `CLAUDE.md`, and
an `AGENTS.md -> CLAUDE.md` symlink.

## 3. Seed only evidenced knowledge

Read the new `_meta/schema.md` and `_meta/workflows.md`. Inspect the smallest
useful set of existing project instructions, READMEs, plans, code, and primary
artifacts. Never read credential files or `.env*`.

Create canonical pages only for claims already supported by those artifacts or
explicitly accepted by the user. Use `synthesized` for agent inference. Preserve
unknowns as questions. Do not bulk-copy documentation, conversations, plans, or
private memory into the repository.

Update `index.md`, `sources/index.md`, and `_meta/log.md` for material bootstrap
content. An empty taxonomy is valid for a genuinely empty project.

Completion criterion: every seeded claim has an appropriate authority and one
canonical home; unsupported sections remain empty.

## 4. Wire both agents into every launch root

Read [agent-routing.md](references/agent-routing.md) and apply its parent router
block to the existing `CLAUDE.md`, adapting only the project name and knowledge
directory. Create `AGENTS.md` as a relative symlink to `CLAUDE.md` when safe. If
either file has different existing semantics, integrate deliberately instead of
replacing it.

Discover every child Git repository inside the parent. Add the reference's
compact child-repository block to each child's existing `CLAUDE.md`, using the
correct relative path to the knowledge repository, and verify or create its
`AGENTS.md -> CLAUDE.md` symlink. This is required because Codex launched inside
a child Git repository stops instruction discovery at that Git root and cannot
see a non-Git parent router.

If the parent is a Git repository, keep the nested knowledge repository out of
the parent's ordinary tracking unless the user explicitly wants a submodule.
Track the parent instruction files in the parent repository when its workflow
allows it. Never initialize Git in the parent merely to satisfy this step.

Completion criterion: fresh Claude and Codex sessions launched from either the
parent or any child repository can identify the same knowledge index and
maintenance workflow.

## 5. Verify and hand off

From the knowledge repository run:

```bash
make lint
make status
git status --short
```

Do not commit or push unless the user requested it. Report the knowledge path,
parent routing files, Git state, checks run, and any unresolved source or layout
question.

Give the user these deterministic first-run prompts:

- Claude Code: `/bootstrap-project-knowledge Initialize the knowledge layer for this workspace.`
- Codex: `$bootstrap-project-knowledge Initialize the knowledge layer for this workspace.`

After installation or edits, recommend a fresh session if the skill does not
appear immediately. Explicit invocation is the bootstrap guarantee; parent
instructions are the ongoing maintenance guarantee.
