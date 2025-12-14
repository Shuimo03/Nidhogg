# Nidhogg

## Overview
Nidhogg is currently in its discovery phase, so this repository focuses on articulating the MVP problem statement, constraints, and collaboration rituals before any runtime code lands. Treat the repo as the single source of truth for the product direction: the `prd/mvp-design.md` document is where requirements, user journeys, and open questions should live, and the rest of the tree (tests, services, tooling) will be layered on as those specs stabilize.

## Repository Layout
- `README.md` – high-level briefing for anyone new to the project and links to the rest of the documentation.
- `prd/mvp-design.md` – product/design notes. Expand this file first whenever the scope, KPIs, or architecture change; even TODO-style outlines are better than tribal knowledge.
- `AGENTS.md` – contributor guide detailing formatting conventions, lint/test commands, and expectations for pull requests.

## How to Work with the MVP Design
1. Start every iteration by reviewing or updating `prd/mvp-design.md`. Capture personas, flows, API contracts, and any relevant diagrams directly in that file (or link to assets checked into the repo).
2. For implementation spikes, sketch the proposed directory layout inside the design doc so reviewers can reason about module boundaries before code is written.
3. Highlight decisions and blockers with bolded callouts (e.g., `**Decision**:`) so new contributors can scan the thread quickly.

## Next Implementation Steps
- Translate the prioritized sections of `prd/mvp-design.md` into tracked issues (features, infrastructure, or experiments) once the MVP scope is locked.
- Introduce a `src/` tree with the first runnable prototype and mirror it with `tests/` so CI can grow incrementally.
- Add concrete build/test commands (Makefile, tox, or justfile) and pin formatter configs (`ruff`, `markdownlint`) to keep subsequent contributions reproducible.
