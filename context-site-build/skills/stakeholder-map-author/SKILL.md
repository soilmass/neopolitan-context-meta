---
name: stakeholder-map-author
description: >
  Authors the project's Stakeholder Map — every named stakeholder
  with role + organization, RACI assignment per major decision class
  (Responsible / Accountable / Consulted / Informed), the escalation
  path, and an influence-vs-interest grid. Writes to
  docs/01-discovery/stakeholder-map.md (site-build-procedure.md
  §3 and §4.2.1 kickoff workshop output). Use at Phase 1 Discovery,
  produced from the kickoff workshop. Do NOT use for: authoring
  personas (use persona-author — stakeholders are
  internal/decision-makers, not end-user segments); authoring the
  project vision (use vision-author); authoring the communications
  plan (Phase 2 §5.7.4 — out of scope here); authoring the risk
  register (use risk-register-author).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.2.0
            Tier 2/3 expansion pass. Modeled on the user-invocable
            draft-stakeholder-map skill but conformed to
            meta-pipeline frontmatter / required-section discipline.
---

# stakeholder-map-author

Phase 1 — produce the project's Stakeholder Map and decision
matrix.

## When to Use

- Phase 1 Discovery; the kickoff workshop has happened; the
  stakeholder map is one of the eight Phase 1 deliverables.
- A new stakeholder enters the project (executive change,
  vendor partnership signed, regulatory body engaged) and the
  RACI must be updated.
- A decision-rights conflict has surfaced ("who decides X?")
  and the map needs to clarify or be re-authored.
- A phase boundary has been crossed and the stakeholder set
  has shifted (e.g., Phase 6 brings in marketing + comms
  stakeholders not present in Phase 1).

## When NOT to Use

- **Persona authoring** — `persona-author`. Personas are
  end-user segments; stakeholders are internal decision-makers
  and external influencers. Don't conflate.
- Project vision — `vision-author`.
- Communications plan (per §5.7.4) — sibling Phase 2
  deliverable. The stakeholder map informs the comms plan
  (who needs what, when) but is its own artifact.
- Risk register — `risk-register-author`. Stakeholder churn
  *is* a risk, but the map and the register are separate.
- Writing meeting agendas — that's a working artifact, not
  this map.
- Drafting a public-facing org chart — the stakeholder map is
  internal-only (it includes decision rights and influence
  candor).

## Capabilities Owned

- Enumerate every **named stakeholder** with role, organization,
  and project relationship: Sponsor, Project Manager, Tech
  Lead, BA, PdM, UX Researcher, designers, engineers, QA,
  Security, Privacy/Legal, content/SEO leads, marketing,
  customer-facing teams, executive owners, vendor partners.
- Assign **RACI** per major decision class (per SOP §3 roles):
  - **R** (Responsible) — who does the work
  - **A** (Accountable) — single named individual who owns
    the outcome (one A per row)
  - **C** (Consulted) — input required before decision
  - **I** (Informed) — kept aware after decision
- Document the **decision-making model** per §4.2.1 kickoff
  output: who decides what, escalation path when blocked.
- Produce the **influence-vs-interest grid**: high influence /
  high interest = manage closely; high influence / low
  interest = keep satisfied; low influence / high interest =
  keep informed; low influence / low interest = monitor.
- Capture **stakeholder-specific concerns**: what success
  looks like for them, what failure costs them, what they
  watch for.
- Note **availability and engagement cadence** — Sponsor
  weekly memo, exec quarterly review, vendor monthly
  sync, etc.
- Cross-reference to the **communications plan** (per §5.7.4)
  once that artifact is authored — the map is the people; the
  plan is the cadence and channel.
- Write to `docs/01-discovery/stakeholder-map.md`.

## Handoffs to Other Skills

- **From the kickoff workshop** (per §4.2.1) — the workshop
  produces the initial stakeholder list and decision-making
  model.
- **To `vision-author`** — the vision is sponsor-approved;
  this map identifies the sponsor.
- **To `risk-register-author`** — stakeholder risks
  (sponsor turnover, executive change, vendor instability)
  surface here and are tracked in the register.
- **To Phase 2 communications plan** (§5.7.4) — the map
  populates the comms plan's stakeholder column.
- **To phase-gate reviews** — every gate has named approvers;
  this map identifies them.
- **From the user-invocable `draft-stakeholder-map`** — peer
  skill.

## Edge Cases

- **Multiple Accountables for one decision class.** Refuse;
  RACI demands a single A per row. Force the choice.
- **Sponsor unclear** ("the leadership team" or "the
  committee"). Halt; this is a §4.1 pre-discovery red flag
  ("Is anyone clearly accountable for the outcome (named,
  willing)?"). Resolve before continuing.
- **Stakeholder count >25.** The map is becoming a directory.
  Cluster into stakeholder *groups* with a named representative
  per group; keep the named-individual list as an appendix.
- **External stakeholder requires NDA-grade discretion.**
  Mark the map's distribution explicitly (internal-only,
  named-people-only) and redact details for shared versions.
- **Conflicting decision rights** between two named
  stakeholders. Halt; the decision-making model needs Sponsor
  arbitration before this map can ship cleanly.
- **Vendor stakeholder is a contracted entity, not a named
  individual.** Capture the contracted entity AND the named
  contact; both are needed for escalation.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §3 (Roles &
Responsibilities) plus §4.2.1 (kickoff workshop output). The
user-invocable `draft-stakeholder-map` is a peer skill
producing the same artifact via a different procedure.

## Self-Audit

Before declaring a stakeholder map complete, confirm:
- Every major decision class has exactly one Accountable
  (single A per RACI row).
- The Sponsor is named (individual, not "the team").
- The escalation path is concrete (Sponsor → CTO → CEO,
  not "we'll figure out").
- Influence-vs-interest grid covers every stakeholder.
- External stakeholders have both an entity AND a named
  contact.
- Distribution policy is stated (internal-only? named-
  people-only? sharable?).
