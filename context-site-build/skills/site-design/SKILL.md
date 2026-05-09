---
name: site-design
description: >
  Routes site-design deliverable-authoring prompts to the right
  atom in the site-design family. Dispatches across all 14 atoms
  covering the Awwwards-tier creative + design-system spine
  (mood board, art direction, concept, motion language, design
  tokens, component states matrix, engineering handoff spec) plus
  Phase 3 design specialists (concept prototyping, wireframes,
  clickable prototype, usability synthesis, a11y annotations) and
  the long-tail (full design system, weekly continuous-discovery
  synthesis). Use when the operator names a design or creative
  deliverable but no specific atom — e.g., "draft the mood board",
  "write the art direction", "spec the motion language". Do NOT
  use for: site-build family deliverables (vision, persona, KPI,
  SRS, ADR, runbook, baseline; use the site-build router); Phase
  4 build sprint planning; Phase 5/6/7 deliverables; meta-pipeline
  lifecycle work (use meta router); domains other than site-design.
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: router
  tags: [router, daily-use]
  changelog: |
    v0.1.0 — initial. Authored as part of family-bootstrap Stage 4
            during the v0.3.0 site-design family bootstrap (Phase
            2 of Option C per docs/ARCHITECTURE-OPTIONS-v0.2.md).
            Routing Table covers all 14 in-family atoms. Family
            scope is Phase 3 design + Awwwards-tier creative
            phases not in the SOP (mood board, art direction,
            concept, motion language) per docs/research/.
---

# site-design

Per-family router for the site-design cluster in the
context-site-build library. Dispatches operator prompts to the
deliverable-authoring atom that owns the artifact.

## When to Use

- The operator names a deliverable (mood board, art direction,
  concept, motion language, design tokens, component states
  matrix, engineering handoff, concept prototype, wireframe,
  clickable prototype, usability test, a11y annotations,
  design system, discovery tick) without specifying which atom
  should produce it.
- The operator describes a phase (Phase 3 Design, Phase 4
  continuous discovery) and the next deliverable to produce
  isn't named.
- The operator says "draft the …", "write the …", "spec the …"
  for any artifact in this family.
- The operator asks "which skill should I use to author X"
  where X is one of the 14 atoms claimed by this family.

## When NOT to Use

- The operator names a specific atom directly
  (`mood-board-author`, `art-direction-author`, etc.) —
  invoke that atom, no routing needed.
- The prompt is about a **site-build family** deliverable
  (vision / persona / KPI / OST / stakeholder map / risk
  register / SRS / ADR / threat model / privacy plan /
  master schedule / runbook / baseline report / weekly
  metric report / change request) — that's the `site-build`
  router in this same library.
- The prompt is about the design-philosophy doc — that lives
  in `site-build/design-philosophy-author` (Tier 3) per the
  v0.1.x decision to keep the strategic philosophy in the
  site-build family. Cross-link rather than duplicate.
- The prompt is about Phase 4 build sprint planning,
  ceremonies, or working software — out of family scope.
- The prompt is about Phase 5/6/7 deliverables — those live
  in `site-build` (current Tier 1) or future `site-operate`
  family.
- The prompt is about meta-pipeline lifecycle — that's the
  `meta` router in `context-meta-pipeline`.
- The prompt is about non-site-design domains (git, postgres,
  etc.).

## Routing Table

| Intent | Target atom |
|---|---|
| Curated visual references with critique / mood board / inspiration set | `mood-board-author` |
| Art Direction document / visual language / palette / type system / motion vocabulary | `art-direction-author` |
| Concept / creative thesis / narrative / lore / creative territory | `concept-author` |
| Motion language / motion tokens / animation principles / easing rules | `motion-language-author` |
| Design tokens / DTCG → Style Dictionary → CSS-vars / Tailwind v4 theme | `design-tokens-author` |
| Per-component 9-state matrix (default…skeleton) | `component-states-matrix-author` |
| Engineering handoff spec / Design→Engineering contract | `engineering-handoff-spec-author` |
| Concept prototype in 3D/runtime tools (Houdini / C4D / WebGL / R3F) | `concept-prototyping-author` |
| Wireframes (lo-fi / mid-fi / hi-fi 3-fidelity ladder) | `wireframe-author` |
| Clickable prototype for usability testing | `prototype-author` |
| Usability test design + synthesis (severity-ranked findings) | `usability-synthesis-author` |
| Per-component accessibility annotations (semantic HTML / ARIA / keyboard / contrast) | `a11y-annotations-author` |
| Full design system documentation (Atomic hierarchy + maintenance discipline) | `design-system-author` |
| Phase 4 weekly continuous-discovery synthesis | `discovery-tick-author` |

All 14 in-family atoms are built (v0.3.0 of library).

## Disambiguation Protocol

When two atoms could plausibly handle a prompt:

- **Mood board vs art direction**: mood board curates *visual
  references with critique*; art direction *synthesizes the
  curation into a defended visual language*. References → mood
  board; defended palette/type/motion vocabulary → art direction.
- **Art direction vs concept**: art direction is the visual
  stance; concept is the creative thesis / narrative. "What does
  this look like" → art direction; "what story does this tell" →
  concept.
- **Concept vs vision** (cross-family): vision (site-build) is
  business-outcome focused; concept (site-design) is creative-
  direction focused. If business outcome is the question → site-
  build router. If creative thesis is the question → concept-author.
- **Motion language vs design tokens**: motion language is the
  motion *contract* (durations, easings, choreography rules);
  tokens are the *encoded values*. Tokens consume motion-language
  outputs. "How does motion behave" → motion-language; "how is
  this expressed in code" → tokens.
- **Design tokens vs design system**: tokens are one input
  (atomic values); system is the whole (Atomic Design hierarchy +
  maintenance + content guidelines). "What's the spacing scale" →
  tokens; "how is this maintained as it grows" → design-system.
- **Component states matrix vs a11y annotations**: states matrix
  bundles a *summary* a11y row per state; a11y annotations are
  the *deep* a11y spec the matrix's row points to. Matrix is the
  9-state grid; annotations go deep on semantic HTML / ARIA /
  keyboard / focus / contrast.
- **Engineering handoff spec vs design system**: handoff is the
  per-feature-area *contract* delivered at Phase 3 close; system
  is the *library-wide spec* that the handoff references. Per-area
  delivery → handoff; library-wide governance → system.
- **Concept prototyping vs clickable prototype**: concept proto
  is in 3D/runtime tools (Houdini / C4D / WebGL) testing
  technical + visual + dynamic feasibility before brief is signed;
  clickable proto is in Figma / Framer testing user-flow
  feasibility for usability research. Different fidelity, tool,
  goal.
- **Wireframes vs clickable prototype**: wireframes are static
  layouts at three fidelities; prototype stitches hi-fi
  wireframes into a navigable flow. Wireframe → "design this
  page"; prototype → "make this clickable for testing."
- **Clickable prototype vs usability synthesis**: prototype is
  *what gets tested*; synthesis is the *analysis of test
  results*. Authoring → prototype-author; analyzing →
  usability-synthesis-author.
- **A11y annotations vs Phase 5 a11y conformance** (cross-
  family): annotations are Phase 3 *design intent*;
  conformance is Phase 5 *post-implementation verification*.
  Conformance is currently out-of-scope for this library
  (deferred to future site-operate or authored ad-hoc); the
  user-invocable `draft-conformance-statement` covers it now.
- **Design system vs design philosophy** (cross-family):
  philosophy (site-build Tier 3) is one-page strategic stance;
  system (site-design Tier 3) is operational documentation
  beyond tokens. Strategic posture → philosophy;
  Atomic-Design + maintenance discipline → system.
- **Discovery-tick vs usability synthesis**: discovery-tick
  is *weekly* Phase 4 synthesis (interviews + analytics +
  support + A/B); usability synthesis is *per-test-round*
  Phase 3 analysis. Weekly cadence → discovery-tick;
  per-prototype-test → usability-synthesis.
- **Discovery-tick vs persona-author / ost-author** (cross-
  family): persona-author + ost-author are Phase 1 synthesis
  (one-time deliverables); discovery-tick is Phase 4 weekly
  cadence. Phase 1 → site-build router; Phase 4 weekly → this
  family.
- **When the prompt spans phases or families**: ask the
  operator which deliverable they're producing right now.
  Routers don't fan out across deliverables; each invocation
  produces one artifact.

## Atoms in This Family

All 14 atoms are built and live (v0.3.0 of library).

**Tier 1 — Essential creative + design-system spine (7):**

- `mood-board-author`
- `art-direction-author`
- `concept-author`
- `motion-language-author`
- `design-tokens-author`
- `component-states-matrix-author`
- `engineering-handoff-spec-author`

**Tier 2 — Specialist (5):**

- `concept-prototyping-author`
- `wireframe-author`
- `prototype-author`
- `usability-synthesis-author`
- `a11y-annotations-author`

**Tier 3 — Long tail (2):**

- `design-system-author`
- `discovery-tick-author`

## Self-Audit

Before declaring a routing decision:

- The chosen atom's `## When to Use` section names the prompt's
  trigger phrasing OR a clear paraphrase.
- The chosen atom's `## When NOT to Use` does NOT exclude the
  current prompt.
- If two atoms could fit, the **Disambiguation Protocol** above
  was consulted and the choice is justified.
- If the prompt is for a cross-family deliverable (vision /
  persona / KPI / SRS / ADR / etc. — site-build family; or
  Phase 5/6/7 deliverables), the operator is told explicitly
  to use the appropriate sibling router or the appropriate
  user-invocable peer.
