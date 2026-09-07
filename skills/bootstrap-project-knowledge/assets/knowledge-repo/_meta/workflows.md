# Agent workflows

## Orient and retrieve

At the start of substantive work:

1. Read `index.md`.
2. Search titles and content for task terminology.
3. Read the smallest useful set of canonical pages.
4. Follow source records only when freshness, precision, or conflict requires it.
5. For an unmigrated topic, use project instructions, code, tests, documents,
   plans, and primary evidence without pretending the knowledge base is complete.

Do not preload the entire repository.

## Query

Identify whether the question asks about meaning, implementation, intent,
current state, or an external fact. Select the matching authority from
`_meta/schema.md`, state uncertainty and time boundaries, and perform the
knowledge-impact check before finishing.

## Knowledge-impact check

Ask:

1. Did the task produce a durable fact, relationship, or reusable lesson?
2. Did evidence invalidate or materially qualify an existing page?
3. Did the user accept, reject, or supersede a decision?
4. Did an initiative's verified state, blocker, or next step change?
5. Was a real question answered or discovered?
6. Did the task expose a contradiction or missing canonical concept?
7. Is the result already represented accurately?

If every answer is no, leave the repository unchanged. Otherwise update the
existing canonical page or create the smallest necessary page, verify the claim,
preserve uncertainty, update the relevant index, and add one concise log entry.

Knowledge maintenance is an in-scope finalization step. It must not trigger an
unrelated decision, deployment, commit, push, or external write.

## Ingest a source

1. Preserve or locate the original without modifying it.
2. Create a source record from `_meta/templates/source.md`.
3. Record identity, origin, date, authority, limitations, and stable reference.
4. Extract only project-relevant claims.
5. Search for every affected canonical page.
6. Update synthesis, decisions, initiatives, or questions as warranted.
7. Preserve contradictions explicitly and update indexes plus the log.

## Promote a conversational result

Promote only conclusions reusable beyond the session. Do not file the transcript.
Distill the supported conclusion, authority, evidence, limitations, affected
canonical page, and remaining uncertainty. Unconfirmed agent inference receives
`status: synthesized`.

## Update an initiative

Verify status from primary delivery evidence. Rewrite current state to describe
only the present, keep one concrete next step, remove resolved blockers, retain
only milestones that explain the present, and log a material update.

## Lint

Inspect broken links, missing index entries, duplicate subjects, stale dates,
unsupported initiative claims, divergent definitions, orphan pages, answered
questions left open, superseded pages presented as active, modified immutable
artifacts, and secret-like content. Lint proposes corrections; it never invents
answers.

## Log format

Use an append-only heading:

```markdown
## [YYYY-MM-DD] update | Subject
```

Allowed operations: `bootstrap`, `ingest`, `update`, `decision`, `query`, `lint`,
and `archive`. Do not log typo or formatting-only edits.
