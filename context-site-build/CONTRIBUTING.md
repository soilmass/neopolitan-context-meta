# Contributing to context-site-build

This library was scaffolded via the meta-pipeline's `library-bootstrap`.
It inherits the meta-pipeline's authoring conventions, validators,
versioning policy, and naming rules.

For any contribution shape:

1. Read the meta-pipeline's [`CONTRIBUTING.md`](../context-meta-pipeline/CONTRIBUTING.md) (parent doc).
2. Run `make verify` from this library's root before submitting.
3. Skill-authoring uses [`skill-author`](../context-meta-pipeline/skills/skill-author/SKILL.md) from the meta-pipeline.
4. Family-bootstrap for whole new domains uses [`family-bootstrap`](../context-meta-pipeline/skills/family-bootstrap/SKILL.md).
5. Restructuring an existing skill uses [`skill-refactor`](../context-meta-pipeline/skills/skill-refactor/SKILL.md).
6. Archiving a skill uses [`skill-retire`](../context-meta-pipeline/skills/skill-retire/SKILL.md).

## Naming convention for skills in this library

Atoms are named `<deliverable>-<verb>` to match the meta-pipeline's
`skill-author`-style pattern. Examples:

- `vision-author` — produces a Vision & Value Proposition document.
- `persona-author` — produces a persona document.
- `kpi-author` — produces a KPI & Success Metrics document.

Routers per family are named after the family itself (e.g., a future
`discovery` router for Phase-1 atoms).

## Audit-finding ledger

This library uses **B-prefixed** finding IDs to distinguish from
the meta-pipeline's `A` series. Every dogfood walkthrough adds rows
to `coverage.md` under "Audit-finding ledger". Findings that
suggest meta-pipeline patches are also cross-referenced into the
meta-pipeline's ledger.
