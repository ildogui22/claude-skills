---
name: knowledge-maintainer
description: Discover, retrieve from, and maintain a project's canonical knowledge base. Use for substantive work in a project that may have an indexed knowledge repository; before completing such work; when durable facts, decisions, initiative state, unresolved questions, domain concepts, systems, or sources must be recorded; and when integrating research or session conclusions into shared knowledge.
---

# Knowledge Maintainer

Keep shared knowledge current without treating it as complete or replacing local
code, tests, instructions, plans, or personal context.

## Discover and retrieve

1. Look for a project knowledge base and its entry point (commonly
   `knowledge/index.md` or `<name>_knowledge/index.md`; the project's CLAUDE.md
   or AGENTS.md usually names it). If none exists, say so and use the project's
   existing documentation conventions; do not create a knowledge system merely
   for this task.
2. Read the index first. Search it and then open only the smallest useful set
   of canonical pages. Read its schema/workflow documentation before creating or
   restructuring pages.
3. For an unmigrated topic, use repository docs, plans, memory, code, tests, and
   primary evidence as fallback. Do not imply the knowledge base is exhaustive.
4. Verify volatile implementation, delivery, and external claims against the
   authority appropriate to the claim. Preserve conflicts and uncertainty.

## Classify before writing

Choose one primary canonical home:

- **Concept:** durable meaning or vocabulary.
- **System:** reusable relationship or cross-component behavior.
- **Decision:** an accepted, proposed, or superseded choice and rationale.
- **Initiative:** current delivery state, next step, or blocker.
- **Question:** a real unresolved or deferred issue.
- **Source:** an original artifact's identity, authority, limitations, and
  immutable reference.

Prefer the existing canonical page. Create the smallest new page only when the
subject has a distinct reusable question or lifecycle. Keep full synthesis in
one place and link from related pages.

## Maintain provenance

Use the knowledge base's required frontmatter, templates, truth model, and log
format. Distinguish observed evidence, accepted decisions, agent synthesis, and
unknowns. Add or update source records when new original evidence matters; do
not file a conversation transcript as evidence. Do not store secrets,
credentials, `.env*` material, private notes, or credential-bearing URLs.

Update pages additively and conservatively: retain useful history, rewrite stale
current state rather than append a diary, and update the index only when pages
are added, moved, archived, or renamed.

## Knowledge-impact check

Before completing substantive work, ask whether it produced a durable fact or
lesson; qualified existing knowledge; accepted/rejected/superseded a decision;
changed verified initiative state; answered or opened a question; or exposed a
contradiction or missing concept. If all answers are no, report that no knowledge
update is needed. Otherwise update the canonical page(s), index when required,
and material log entry.

Validate a knowledge edit with whatever check the knowledge base defines for
itself (often `make lint` and `make status` run from the knowledge directory);
run its integration check when available. Do not treat a
router or reminder as proof that this workflow occurred: only a hook enforces
the operations it explicitly performs.

## Report

State the pages and source records updated, evidence checked, and remaining
uncertainty. If no update was needed, say so explicitly and give the result of
the impact check.
