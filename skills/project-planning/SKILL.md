---
name: project-planning
description: Shape a greenfield project or major initiative before implementation. Use when starting a new build, migration, redesign, or architectural change whose route may require dependent product, domain, research, or prototype decisions; also use when repository exploration reveals that an ordinary implementation plan would rely on unresolved assumptions or span multiple agent sessions.
---

# Project Planning

Route planning by uncertainty. Keep ordinary work light; use Wayfinding only when
the destination is visible but the route is not.

## 1. Inspect the effort

Read applicable project instructions, the smallest relevant repository surface,
existing plans or maps, and the canonical knowledge index when one exists. Resolve
discoverable facts from those sources instead of asking the user.

If an active map already covers the effort, take the **Continue** branch. Otherwise
identify the destination, acceptance signal, affected systems, unresolved choices,
evidence gaps, and likely reversibility of early decisions.

Completion criterion: the planning mode can be selected from concrete evidence,
not from adjectives such as “big” or “complex.”

## 2. Select the planning mode

Use **ordinary planning** when the route can be decomposed without guessing: the
destination and acceptance signal are clear, dependencies are understood, and no
research, prototype, or human decision blocks implementation. Project size alone
does not justify Wayfinding. State the reason briefly and continue with the normal
planning or implementation workflow.

Use **Wayfinding** when either condition holds:

- An implementation sequence would assume an unresolved product, domain, or
  architectural decision.
- Two or more unresolved decisions depend on one another.

Also use it when at least two supporting signals hold:

- Critical research or a prototype must precede a decision.
- The effort is likely to cross agent sessions and needs durable decision state.
- Several systems or independently workable frontiers are involved.
- An early choice would be expensive to reverse.
- The scope or acceptance signal remains materially unclear after inspection.

When Wayfinding applies, read [references/wayfinding.md](references/wayfinding.md)
completely and take the **Chart** or **Continue** branch defined there.

Completion criterion: exactly one planning mode is chosen and its next action is
clear.

## 3. Route specialist work

Delegate the substance of a decision ticket to the existing skill that owns it:

- Use `grilling` for a human decision and `domain-modeling` when vocabulary,
  boundaries, or architecture crystallize.
- Use `research` for facts outside the current working tree.
- Use `prototype` when a rough artifact will make behavior or appearance decidable.
- Use `knowledge-maintainer` to retrieve prior truth and promote accepted durable
  conclusions; keep active map state outside canonical knowledge.
- Use `bootstrap-project-knowledge` only when the user wants or the project needs a
  shared cross-agent knowledge repository; that skill owns its creation and wiring.
- Use `tdd` or the relevant implementation skill only after the route is clear, or
  when the map's Notes explicitly include execution.

Invoke those skills rather than restating their procedures here.

Completion criterion: every specialist action has one owner and one resulting
artifact or resolution.

## 4. Hand off to implementation

Before declaring the route clear, verify that:

- the destination and acceptance signal are agreed;
- material scope boundaries and domain terms are explicit;
- consequential or hard-to-reverse decisions are resolved;
- blocking evidence and prototype questions are answered;
- remaining unknowns can safely be decided during implementation; and
- public interfaces or test seams are identified where they matter.

Then mark the map complete, preserve its decision pointers, and produce the normal
implementation plan. Run the knowledge-impact check before finishing substantive
work and use `handoff` when the user closes the session.

Completion criterion: implementation can proceed without silently inventing a
material decision.
