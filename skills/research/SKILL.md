---
name: research
description: Investigate a question against high-trust primary sources and integrate durable findings into the project's canonical knowledge base. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

Use an available background/subagent mechanism when it improves the research;
do not assume a tool-specific agent implementation.

Its job:

1. Investigate the question against **primary sources** — official docs, source code, specs, first-party APIs — not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Invoke `knowledge-maintainer` when the project has a knowledge base. Create
   source records for material original evidence and integrate reusable findings
   into existing canonical concepts, systems, decisions, initiatives, or
   questions. Preserve provenance, authority, and limitations.
3. Do not create an isolated report when the findings belong in canonical
   knowledge. Use a repo-local research note only when it is explicitly needed
   and link it from the relevant canonical record.
4. Report the primary evidence, canonical pages affected, and uncertainty.
