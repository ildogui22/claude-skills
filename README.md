# claude-skills

Claude Code skills, kept here so they can be picked up on another machine.

To use one, copy its directory into `~/.claude/skills/` and restart Claude Code.

```bash
cp -R skills/grilling ~/.claude/skills/
```

## The skills

| Skill | What it does |
|---|---|
| `knowledge-maintainer` | Read from and maintain a project's canonical knowledge base |
| `bootstrap-project-knowledge` | Scaffold a new knowledge repo — templates, index, schema, validators |
| `project-planning` | Route planning by uncertainty; Wayfinding when the route isn't visible |
| `domain-modeling` | Sharpen ubiquitous language; write glossary entries and ADRs |
| `research` | Investigate against primary sources, integrate durable findings |
| `handoff` | End-of-session ritual so nothing important dies with the context |
| `tdd` | Red/green loop, and what makes a test worth keeping |
| `diagnosing-bugs` | Phased diagnosis loop for hard bugs and perf regressions |
| `prototype` | Throwaway code that answers one question |
| `resolving-merge-conflicts` | Resolve conflicts by recovering intent, never by inventing behaviour |
| `grilling` | Relentless one-question-at-a-time interview to stress-test a plan |
| `grill-me` | User-invocable alias for `grilling` |
| `writing-great-skills` | Meta-skill: what makes a skill predictable. Read before editing the others |

**One dependency worth knowing:** `knowledge-maintainer` is the hub — `tdd`,
`diagnosing-bugs`, `domain-modeling`, `research`, `handoff` and
`project-planning` all invoke it by name, so take it along with any of those.
`grilling`, `grill-me`, `resolving-merge-conflicts`, `prototype` and
`writing-great-skills` stand alone.
