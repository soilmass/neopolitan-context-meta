# site-design Coverage

Authority (composite):
- Primary: `internal://site-build-procedure.md` §6 (Phase 3 — Design)
  — Edison Steele — "Website & Web Application Build Procedure
  (v2.0)"; canonical local path
  `/home/edox1/Public/neopolitan/docs/claude-docs/site-build-procedure.md`.
- Secondary: `internal://docs/research/SYNTHESIS.md` (Awwwards-tier
  research, 2026-05-08) — adds named phases the SOP doesn't have
  (mood board, art direction, concept, motion language) per ~20
  agency methodologies surveyed.

Last verification: 2026-05-09 (initial bootstrap; all 14 in-family
atoms authored).

## In Scope (Tier 1) — 7 atoms

| Atom | Owns | Last health check |
|---|---|---|
| `mood-board-author`              | Mood Board + curated Reference list with critique (E2 §C.1 Lusion Phase 1) | 2026-05-09 (fresh) |
| `art-direction-author`           | Art Direction document — palette, type, motion vocabulary (E2 §A.3 + glossary) | 2026-05-09 (fresh) |
| `concept-author`                 | Concept — creative thesis, narrative, lore, defended creative territory (E2 §A.2 + §C) | 2026-05-09 (fresh) |
| `motion-language-author`         | Motion Language — durations, easings, choreography, motion tokens (E3 §6.3; SOP §6.4.1 motion partial) | 2026-05-09 (fresh) |
| `design-tokens-author`           | DTCG → Style Dictionary v4 → CSS-vars + Tailwind v4 + TS types pipeline (E3 §6.1; SOP §6.4.1) | 2026-05-09 (fresh) |
| `component-states-matrix-author` | Per-component 9-state matrix (default…skeleton) (E3 §6.2; SOP §6.4.3) | 2026-05-09 (fresh) |
| `engineering-handoff-spec-author`| Engineering Handoff Spec — Design→Engineering contract (SOP §6.6) | 2026-05-09 (fresh) |

Plus the per-family router `site-design` (archetype: router; v0.1.0; fresh).

## In Scope (Tier 2) — 5 atoms

| Atom | Owns | Last health check |
|---|---|---|
| `concept-prototyping-author`     | Concept prototype in 3D / runtime tools (Houdini / C4D / WebGL / R3F) (E2 §C.2 Lusion Phase 2) | 2026-05-09 (fresh) |
| `wireframe-author`               | Wireframes across 3 fidelities — lo-fi / mid-fi / hi-fi (E2 §C.4 Hello Monday; SOP §6.2) | 2026-05-09 (fresh) |
| `prototype-author`               | Clickable prototype for usability testing (SOP §6.3.1) | 2026-05-09 (fresh) |
| `usability-synthesis-author`     | Usability test design + synthesis (severity-ranked findings) (SOP §6.3.2 + §6.3.3) | 2026-05-09 (fresh) |
| `a11y-annotations-author`        | Per-component accessibility annotations on hi-fi designs (SOP §6.4.5) | 2026-05-09 (fresh) |

## In Scope (Tier 3) — 2 atoms

| Atom | Owns | Build trigger | Last health check |
|---|---|---|---|
| `design-system-author`           | Full design system documentation — Atomic Design hierarchy + maintenance discipline (SOP §6.4 full) | Project has ≥3 templates AND tokens + matrices + a11y annotations exist | 2026-05-09 (fresh) |
| `discovery-tick-author`          | Phase 4 weekly continuous-discovery synthesis (SOP §7.5 + §2.3) | Phase 4 begins AND product trio commits to weekly cadence | 2026-05-09 (fresh) |

## Specced, Not Yet Built

None — all 14 in-family atoms are now built.

## Policy Overlay

No policy overlay exists for this family yet. Stack-specific
overlays (`house-site-design-r3f`, `house-site-design-figma`,
etc.) are queued for Phase 4 of the v0.2.x expansion plan per
`docs/ARCHITECTURE-OPTIONS-v0.2.md`. Authoring goes through
`skill-policy-overlay` in the meta-pipeline.

## Out of Scope

| Capability | Why out of scope | Where to look instead |
|---|---|---|
| `design-philosophy-author` | Already authored in site-build Tier 3; cross-link from this family's atoms rather than duplicate | `site-build/design-philosophy-author` |
| `design-qa-checklist` | Folds into `a11y-annotations-author` + `component-states-matrix-author` + the Stage 6 family audit | (folded) |
| `design-handoff-walkthrough` | Folds into `engineering-handoff-spec-author`'s Capabilities Owned (the meeting is part of the spec) | (folded) |
| `responsive-behavior-rules` | Folds into `component-states-matrix-author` + `design-system-author` | (folded) |
| Phase 4 build deliverables (sprint planning, working software per sprint, sprint review notes) | Build-phase ceremonies are out of scope for site-design | (would belong to a future `site-execute` family or stay manual) |
| Phase 5 a11y conformance statement | Post-implementation verification artifact (Phase 5 hardening); annotations here are *design intent* | Future `site-operate` family OR direct `skill-author` invocation |
| Phase 5/6/7 other deliverables (runbooks, launch comms, baseline reports, weekly reports, optimization backlog) | Belong to `site-build` family (current Tier 1) or future `site-operate` family | `site-build` family + future `site-operate` |
| Polish discipline + Awards submission | Awwwards-tier "secret-sauce" phases that operate post-design (during launch / hardening) | Future `site-operate` family |
| Stack-specific styling decisions (Tailwind config, CSS architecture, component implementations) | Phase 4 build territory | Project's own repo + future stack overlays |
| The website code itself | Build artifact, not methodology output | Project's own repo |

## Coverage Matrix Status

Last `skill-audit` run: 2026-05-09 (Stage 6 advisory audit during
family-bootstrap).

- Tier 1 (7 atoms): all `fresh` (just authored); audit in P2.6.
- Tier 2 (5 atoms): all `fresh`; audit in P2.6.
- Tier 3 (2 atoms): all `fresh`; audit in P2.6.
- Router `site-design`: `fresh`.

Tier transitions since last verification: none (initial bootstrap).
14-atom family fully built at v0.1.0; no Specced-Not-Yet-Built
queue carried forward.
