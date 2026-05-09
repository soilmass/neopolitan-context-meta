# site-design family — taxonomy

Stage 3 artifact for `family-bootstrap`. Tiered groups of atoms per
`../../context-meta-pipeline/skills/family-bootstrap/references/tier-model.md`.

The site-design family covers Phase 3 design + the **Awwwards-tier
upstream phases** that govern visual direction before wireframes
begin. The methodology spine is the SOP's §6 (Phase 3 Design); the
Awwwards-tier additions (mood board, art direction, concept, motion
language) come from `docs/research/E2-agency-methodologies.md`,
where ~20 top agencies treat them as first-class deliverables that
distinguish award-winning work from generic web work.

Authority (composite):
- Primary: `internal://site-build-procedure.md` §6 (Edison Steele)
- Secondary: `docs/research/SYNTHESIS.md` (Awwwards-tier research,
  2026-05-08)

---

## Tier 1 — Essential (7 atoms)

Every Awwwards-tier project authors all of these. They form the
load-bearing spine across the creative + design-system phases.

| Atom | Role | Primary cite |
|---|---|---|
| `mood-board-author`              | Curated visual references with critique — "what works and why"      | E2 §C.1 (Lusion Phase 1) |
| `art-direction-author`           | Art Direction doc — visual language, palette, type, motion vocab    | E2 §A.3 + glossary |
| `concept-author`                 | Concept — creative direction, narrative, lore, creative territory   | E2 §A.2 + §C (Lusion, Resn, Antinomy, AT) |
| `motion-language-author`         | Motion Language — timing, easing, choreography rules + motion tokens| E3 §6.3 motion specs |
| `design-tokens-author`           | DTCG JSON → Style Dictionary → CSS-vars + Tailwind v4 + TS types    | E3 §6.1; SOP §6.4.1 |
| `component-states-matrix-author` | 9-state matrix per component (default…skeleton)                     | E3 §6.2; SOP §6.4.3 |
| `engineering-handoff-spec-author`| Design→Engineering contract at end of Phase 3                       | E3 §6.6; SOP §6.6 |

## Tier 2 — Specialist (5 atoms)

| Atom | Role | Primary cite |
|---|---|---|
| `concept-prototyping-author`     | 3D/runtime concept prototype (Houdini / C4D / vvvv / WebGL) — distinct from clickable Figma proto | E2 §C.2 (Lusion Phase 2) |
| `wireframe-author`               | Wireframes across 3 fidelities (lo/mid/hi); paper → blocks → visual | E2 §C.4 (Hello Monday); SOP §6.2 |
| `prototype-author`               | Clickable prototype (Figma/Framer/coded) for usability testing      | SOP §6.3.1 |
| `usability-synthesis-author`     | Usability test synthesis — severity-ranked issues with recommended fixes | SOP §6.3.3 |
| `a11y-annotations-author`        | Per-component accessibility annotations on hi-fi designs            | SOP §6.4.5 |

## Tier 3 — Long tail (2 atoms)

| Atom | Build trigger | Primary cite |
|---|---|---|
| `design-system-author`           | Project has ≥3 templates AND tokens + states matrix exist; full design-system doc warranted | SOP §6.4 (full) |
| `discovery-tick-author`          | Phase 4 begins AND weekly continuous-discovery cadence committed     | SOP §7.5 + §2.3 |

---

## In-family total

7 + 5 + 2 = **14 atoms.** Within the 12-21 cap declared by
family-bootstrap Stage 3 gate.

Router: `site-design` (per-family router; archetype=router; lists
all 14 atoms in its Routing Table).

---

## Out of Scope (this family)

The 3 capabilities below were considered and explicitly out-of-
scoped for this family — they fold into existing atoms or belong
to a different family.

| Capability | Why out of scope | Where it lives instead |
|---|---|---|
| `design-philosophy`              | Already authored in site-build Tier 3; cross-link from this family's atoms rather than duplicate | `site-build/design-philosophy-author` |
| `design-qa-checklist`            | Folds into `a11y-annotations-author` + `component-states-matrix-author` + the Stage 6 family audit | (folded) |
| `design-handoff-walkthrough`     | Folds into `engineering-handoff-spec-author`'s Capabilities Owned (the hand-off meeting is part of the spec, not separate) | (folded) |
| `responsive-behavior-rules`      | Folds into `component-states-matrix-author` + `design-system-author` (responsive is a per-component concern, not a family-level deliverable) | (folded) |
| Phase 4 build deliverables (sprint planning, working software per sprint, sprint review notes) | Different family; build-phase ceremonies are out of scope for site-design | (would belong to a future `site-build-execute` family or stay manual) |
| Phase 5/6/7 deliverables (a11y conformance, runbooks, launch comms, baseline reports) | Belong to `site-build` family (current Tier 1) or future `site-operate` family | `site-build` family + future `site-operate` |
| Polish discipline + Awards submission | Awwwards-tier "secret-sauce" phases that operate post-design (during launch / hardening). Belong to future `site-operate` family | future `site-operate` family |

---

## Stage 3 gate self-check

- ✓ Every capability from `capabilities.json` lands in exactly one tier OR Out of Scope.
- ✓ Tier 1 size: 7 (within 6-9).
- ✓ Tier 2 size: 5 (within 4-7).
- ✓ Tier 3 size: 2 (within 2-5).
- ✓ Every Tier 3 entry has an observable build trigger.
- ✓ Every Out-of-Scope entry names where it lives instead.

---

## Notes

- **Atom naming**: atoms use `<deliverable>-author` matching the
  site-build family's convention.
- **Relationship to site-build family**: site-design is the design+
  creative phase of the methodology; site-build covers the strategic
  spine (Phase 1+2 + selected Phase 5/6/7 atoms). The two families
  are siblings within `context-site-build` and cross-reference at
  Phase boundaries (e.g., `design-philosophy-author` in site-build
  Tier 3 hands off to this family's Tier 1 atoms).
- **Relationship to draft-* user-invocable peers**: each atom names
  its `draft-*` peer (e.g., `draft-design-system-tokens` for
  `design-tokens-author`) per the v0.1.2 self-review convention
  (B6/A62 — anti-trigger fallback to user-invocable peer).
