---
name: cross-domain-orchestrator-author
description: >
  Authors an orchestrator skill that spans two families *within the
  same library* (e.g., an incident workflow combining the logs family
  and the metrics family). Produces the orchestrator archetype's
  required sections plus per-family handoff documentation. Do NOT use
  for: workflows spanning two libraries (use cross-library-orchestrator);
  authoring a single skill (use skill-author); bootstrapping a new
  family (use family-bootstrap); pattern-extracting a meta-orchestrator
  from N existing ones (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: tool
  tags: [composition, rare]
  changelog: |
    v0.1.1 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy plus `references/orchestration-patterns.md` (speculative; pre-trigger disclaimer at top of each).
    v0.1.0 — initial. Authored as part of v0.5.0 kitchen-sink meta-tooling release.
            Build trigger had not yet fired (zero cross-domain orchestrators
            exist); tool ships ahead of trigger to claim the surface area.
            Per ARCHITECTURE.md §"Cross-domain orchestrator template" the
            pattern itself extracts only after 2-3 hand-authored examples.
---

# cross-domain-orchestrator-author

The Tier 1 tool for authoring cross-domain orchestrators within a
single library. Companion to `cross-library-orchestrator` (which
spans libraries).

## Purpose

Some workflows span two domain families inside one library: an
incident-response workflow that combines the logs family + the
metrics family + git history; a release workflow that combines the
build family + the test family + the deploy family. When two
families coexist, an orchestrator can compose them.

This tool authors the orchestrator SKILL.md with explicit per-family
handoff documentation, so the cross-family contract is visible
rather than buried in the orchestrator's prose.

## When to Use

- Two or more families coexist in the same library.
- A real workflow has emerged that spans them (≥2 actual usage
  occurrences, not speculative).
- The workflow is repeated and worth standardizing.

## When NOT to Use

- For workflows spanning two libraries — use
  `cross-library-orchestrator`.
- For workflows within a single family — use the family's existing
  router and handoffs; don't wrap in an orchestrator.
- For authoring a single skill — use `skill-author`.
- For bootstrapping a new family — use `family-bootstrap`.
- Speculatively, "we might want this someday" — author against real
  cases. Per `ARCHITECTURE.md`, the meta-pattern itself is deferred
  until 2-3 hand-authored cross-domain orchestrators exist; the
  first 2-3 are intentionally per-orchestrator authoring runs.

## Stage-Gated Procedure

Five stages.

### Stage 1 — Workflow intake

**Consumes:** the operator's prompt naming the workflow + the
families involved.

**Produces:** `cross-domain-intake.yaml` with
- `name` — the orchestrator's name.
- `families` — list of families (router skills) involved.
- `skills` — for each family, the specific atoms the orchestrator
  will call.
- `workflow` — sequence of stages, each naming the family + atom +
  handoff condition.

**Gate:** every named family has a router in the consuming library;
every named atom resolves; the workflow has ≥2 stages spanning ≥2
families.

### Stage 2 — Handoff design

**Consumes:** Stage 1 + the families' `coverage.md` files.

**Produces:** `handoff-design.md` documenting
- For each cross-family edge: what data passes; what state changes
  occur in each family.
- Whether the handoff is one-way (family A → family B) or
  bidirectional.
- Whether either family's `## Handoffs to Other Skills` already
  references the other (if not, this is a Stage 5 weaving update).

**Gate:** every handoff has an explicit data-shape; bidirectional
handoffs name both directions explicitly.

### Stage 3 — Delegate to skill-author

**Consumes:** Stages 1-2.

**Produces:** the orchestrator SKILL.md authored via `skill-author`
archetype=`orchestrator`. Pre-fills:
- `Purpose` — derived from intake
- `When to Use` / `When NOT to Use` — anti-trigger fences other
  orchestrators (and `family-bootstrap` itself, which is *not* a
  cross-domain orchestrator)
- `The Stages` — from the workflow sequence
- `Skills Coordinated` — every cross-family atom, qualified by family
- `Failure Modes` — what happens when each family's atom fails
- `Handoffs` — explicit cross-family handoff list

**Gate:** `validate-metadata.py` exits 0; `## Skills Coordinated`
names every atom with family qualifier (e.g., `logs/log-search` +
`metrics/metric-query`).

### Stage 4 — Family handoff weave-back

**Consumes:** Stage 3's SKILL.md + each involved family's atoms.

**Produces:** updates to each involved atom's
`## Handoffs to Other Skills` section noting that this orchestrator
exists as a higher-level composition. This makes the cross-family
relationship discoverable from either end.

**Gate:** every involved atom now references this orchestrator in
its `## Handoffs` section (or has an explicit "no handoff back"
justification).

### Stage 5 — Verify + capture pattern

**Consumes:** the post-authoring state.

**Produces:** the output of `verify.sh` plus a one-paragraph
contribution to `<library>/coverage.md` §"Cross-Domain Orchestrators"
naming this orchestrator and the families it composes.

**Gate:** `verify.sh` exit 0; the coverage row is added; if this is
the 2nd or 3rd cross-domain orchestrator in the library, an open
question lands in `ARCHITECTURE.md` §"Cross-domain orchestrator
template" about whether the pattern is now extractable.

## Dependencies

- `skill-author` — Stage 3 delegation.
- `scripts/validate-metadata.py` — Stage 3 gate.
- `verify.sh` — Stage 5.
- The consuming library's `coverage.md` — Stage 5 update.

## Evaluation

`cross-domain-orchestrator-author` is correct when, run against a
synthetic two-family scenario, the produced orchestrator:

1. Passes `validate-metadata.py` exit 0.
2. Names every cross-family atom in `## Skills Coordinated` with
   family qualifier.
3. Has explicit handoff documentation (data-shapes, not just prose).
4. Each involved family's atoms reference back to this orchestrator
   in their own `## Handoffs to Other Skills`.
5. The coverage.md `## Cross-Domain Orchestrators` row is added.

The first dogfood is whenever a consuming library authors its first
cross-domain orchestrator. Until then, the tool is exercised against
synthetic fixtures.

## Handoffs

- **From the operator** — direct invocation when a real cross-family
  workflow emerges.
- **To `skill-author`** — Stage 3 delegation.
- **To `library-audit`** — the new orchestrator is in scope for the
  audit's snapshot integrity check.
- **To `ARCHITECTURE.md` §"Cross-domain orchestrator template"** —
  Stage 5's open-question contribution accumulates evidence for
  the eventual pattern extraction.
