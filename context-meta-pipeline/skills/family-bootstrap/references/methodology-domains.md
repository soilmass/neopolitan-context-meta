# Methodology domains

Surfaced by audit finding A58 (2026-05-08, first real-consumer
dogfood of `library-bootstrap` + `family-bootstrap` against the
`context-site-build` library).

## What this reference covers

The default mental model for picking a family domain assumes a
**technical domain** — `git`, `postgres`, `kubectl` — where:

- Capabilities are operations on a single tool or system.
- Each capability is small (one command flag, one error mode).
- The domain naturally has 10-30 lifted capabilities, fitting one
  family.

This reference covers the common-but-distinct case: **methodology
domains** — site-build / SOX-compliance / clinical-trial-protocols /
ITIL / etc. — where:

- Capabilities are heavyweight deliverables (one document, one
  artifact).
- Each capability is large (a vision document, an SRS, a runbook).
- The domain naturally has 20-50 capabilities total, but per-phase
  it has only 1-7. **Phase-per-family is the obvious-but-wrong cut.**

## Why phase-per-family fails

The Stage 2 gate requires ≥10 capabilities indexed. A phase-per-family
cut typically produces:

- Phase 1 (discovery): 5-7 deliverables — **below gate**
- Phase 5 (hardening): 1-2 deliverables — **below gate**
- Phase 6 (launch): 1-2 deliverables — **below gate**
- Phase 7 (post-launch): 8-12 deliverables — fits

A library trying to bootstrap 7 families to cover the methodology
will fail Stage 2 on most of them.

## The right cut: one family with phase-organized tiers

Methodology domains typically fit best as **one family** named for
the methodology, with **phase-organized Tier 1 / 2 / 3** atoms:

- **Tier 1**: the methodology spine — one anchor deliverable per
  major phase (vision / SRS / ADR / runbook / baseline-report).
- **Tier 2**: specialist deliverables across phases (KPI / threat
  model / privacy plan / risk register).
- **Tier 3**: long-tail deliverables (OST, design-philosophy, change
  request).

If the methodology is large enough that one family genuinely
overflows the 12-21 atom cap, the natural split is **two-or-three
families clustered by phase group** (not one per phase):

- `<methodology>-planning` — Phase 1 + 2 deliverables.
- `<methodology>-design` — Phase 3 + 4 deliverables (if non-trivial).
- `<methodology>-operate` — Phase 5 + 6 + 7 deliverables.

Each cluster typically has 12-18 capabilities, fitting Stage 2's gate.

## Indicators you have a methodology domain

- Each capability produces a **document or artifact** as its primary
  output, rather than performing an operation.
- The capabilities have a **temporal ordering** (Phase 1 before
  Phase 2 before Phase 3, etc.).
- The authority is a **single SOP document** (not a tool's API docs).
- The total capability count is in the 20-50 range, not 10-30.

## Indicators you have a technical domain

- Each capability is an **operation** on a system or artifact (not
  itself an artifact).
- Capabilities can run in any order; there is no temporal spine.
- The authority is **API docs** or **a tool's own documentation**.
- The total capability count is 10-30; one family fits cleanly.

## Authority pattern for methodology domains

The Stage 1 gate requires `authority.url` + `authority.author`. For
methodology domains the canonical authority is often a private SOP
without a public URL. The `internal://` URI convention (audit finding
A59) handles this case; it is documented in the family-bootstrap
intake checklist.
