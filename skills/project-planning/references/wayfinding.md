# Wayfinding branch

This branch adapts the planning mechanics of Matt Pocock's official Wayfinder skill:

- Current upstream: <https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md>
- Revision inspected: `38d62e71ed01fc05d5ae63b0807172e9546049d5`
- Inspected: 2026-08-15

Use the upstream source—not summaries or videos—when checking semantics or drift.
This adaptation adds an automatic complexity gate, cross-agent knowledge routing,
and an implementation-readiness gate; those additions are local, not upstream
Wayfinder behavior.

## Invariants

- Wayfinding resolves decisions before execution. A ticket is a question or
  investigation, not a slice of the destination to build.
- One map represents one project or major initiative.
- The map is a low-resolution index. Ticket detail and resolution live with the
  ticket; the map contains only a named pointer and one-line gist.
- Refer to maps and tickets by descriptive title. Keep ids or URLs inside links.
- Load the map once per session, then zoom into only the selected ticket and the
  context it requires.
- Work one non-research ticket per session. Independent research tickets may run in
  parallel when the environment permits it.
- A human-in-the-loop ticket is resolved by the human-agent exchange. The agent does
  not manufacture the human's answer.

## Storage

Use the repository's configured issue tracker when it already supports child issues,
blocking, assignment, and frontier queries. Use its native relationships.

Otherwise use a local Markdown tracker:

```text
planning/wayfinding/<initiative>/
├── map.md
└── tickets/
    └── <ticket-title>.md
```

Do not introduce or connect an external tracker solely for Wayfinding. For local
tickets, express status, type, blockers, and claim in frontmatter. An open ticket is
on the **frontier** when all blockers are closed and it is unclaimed.

## Map shape

```markdown
# <Map title>

## Destination

<The observable spec, decision, or changed state this effort is finding a route to.>

## Notes

<Standing constraints, relevant skills, domain, and whether execution is included.>

## Decisions so far

- [<Resolved ticket title>](link) — <one-line gist>

## Not yet specified

<In-scope fog that cannot yet be phrased as a precise question.>

## Out of scope

<Consciously excluded work and the reason it lies beyond this destination.>
```

Open tickets are found through the tracker, not duplicated in the map.

## Ticket shape

```markdown
---
status: open
type: research | prototype | grilling | task
blocked_by: []
claimed_by:
---

# <Decision ticket title>

## Question

<The single decision or investigation this ticket resolves.>

## Resolution

<Filled when resolved; link assets instead of pasting them.>
```

Size the question for one focused agent session. Create tickets first, then wire
blocking relationships after every ticket has an identity.

Ticket types route as follows:

- **Research (agent-driven):** establish a fact a decision awaits; use `research`.
- **Prototype (human-in-the-loop):** make behavior or appearance concrete; use
  `prototype` and link the throwaway artifact.
- **Grilling (human-in-the-loop):** resolve a choice through conversation; use
  `grilling` and `domain-modeling`.
- **Task (agent- or human-driven):** perform prerequisite work that exposes facts
  needed for a later decision. It earns a ticket by unblocking a decision.

## Chart

1. Name the destination with `grilling` and `domain-modeling`. Let the destination
   fix scope.
2. Explore breadth-first to surface precise questions and dependencies. If the route
   is already clear and contains no material fog, return to ordinary planning.
3. Create the map with Destination and Notes; sketch only genuine fog under Not yet
   specified.
4. Create every question that is precise now as a ticket. Wire blockers in a second
   pass so the frontier becomes visible.
5. Resolve independent research tickets in parallel when useful and safe. Preserve
   their findings through the `research` and `knowledge-maintainer` contracts.
6. Finish charting with the map and frontier established. Begin execution only when
   Notes explicitly make execution part of this effort.

Chart breadth-first across the map, but conduct live decision work through the
owning skill. When a human answer is needed, begin the highest-leverage `grilling`
ticket and ask its single next question; leave the remaining questions visible as
tickets instead of presenting them as a batch questionnaire.

Completion criterion: collaborators can see the destination, the takeable frontier,
the blocked questions, the fog, and the scope boundary without loading every ticket.

## Continue

1. Load the low-resolution map and query the current frontier.
2. Use the ticket named by the user; otherwise claim the first suitable unblocked,
   unclaimed ticket before working it.
3. Resolve it with the owning specialist skill, retrieving detailed context only as
   needed.
4. Record the resolution with the ticket and close it. Add its named pointer and gist
   to Decisions so far; promote durable accepted truth through `knowledge-maintainer`.
5. Re-map the frontier. Graduate newly precise fog into tickets, update invalidated
   tickets, and move work beyond the destination to Out of scope.
6. Apply the readiness gate in `SKILL.md` when the map has no material frontier or
   fog remaining.

Completion criterion: the selected ticket has one authoritative resolution and the
map accurately exposes the next frontier or the implementation handoff.

## Fog and scope

A precise unanswered question is a ticket, even when blocked. A suspected area that
cannot yet be stated as a precise question remains in Not yet specified. When a prior
answer makes it precise, remove it from the fog and create the ticket.

Fog lies toward the destination. Work beyond the destination belongs in Out of scope
and never graduates unless the destination is deliberately redrawn as a new effort.
