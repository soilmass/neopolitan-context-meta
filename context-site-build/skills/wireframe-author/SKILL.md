---
name: wireframe-author
description: >
  Authors wireframes across three fidelities — low-fi (paper
  sketches / Figma blocks; structure only), mid-fi (real content
  + labels; flow review), and high-fi (visual design applied;
  responsive breakpoints; all interactive states). Output goes to
  docs/03-design/wireframes/<area>-{lo,mid,hi}.md plus the linked
  Figma files (SOP §6.2; research/E2 §C.4). Use across Phase 3
  Design after art-direction-author and concept-author run. Do
  NOT use for: authoring the visual language (use art-direction-
  author); authoring the concept (use concept-author); authoring
  clickable prototypes for usability testing (use prototype-
  author — prototypes stitch hi-fi wireframes into a flow);
  per-component state matrices (use component-states-matrix-
  author); production code (Phase 4 build).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C).
---

# wireframe-author

Phase 3 — produce wireframes for one feature area across three
fidelities.

## When to Use

- Phase 3 Design is in progress; art direction + concept have
  shipped; the IA is locked from Phase 2; one or more feature
  areas need wireframing.
- A new feature area is being added mid-Phase-3 and needs the
  3-fidelity ladder.
- A user research finding has invalidated existing wireframes
  and a feature area needs re-wireframing at the appropriate
  fidelity.
- A pitch / sponsor preview needs visual evidence at hi-fi
  before formal Phase 3 Gate.

## When NOT to Use

- IA / sitemap / user flows don't exist — those are Phase 2
  outputs (per `srs-author` §5.2). Wireframing without IA is
  inventing structure rather than implementing it.
- Authoring the visual language — `art-direction-author`. Hi-fi
  wireframes apply art direction; they don't define it.
- Authoring the concept — `concept-author`. Concept governs
  narrative; wireframes are structural.
- Generating clickable prototypes for usability testing —
  `prototype-author`. Prototypes stitch hi-fi wireframes into
  navigable flows.
- Per-component state matrices — `component-states-matrix-
  author`. Wireframes show layouts; matrices show component
  states.
- Production code — Phase 4 build.
- Skipping fidelities. Per SOP §6.7 anti-pattern: "Skipping
  low-fi means visual debate masks structural problems." This
  atom refuses to ship hi-fi without lo-fi having been
  reviewed first.

## Capabilities Owned

- Author **low-fidelity wireframes** (per SOP §6.2.1):
  - Grayscale, layout only.
  - Paper sketches or simple Figma blocks.
  - Confirms IA is workable on the page.
  - Reviewed for *structure* and *information hierarchy*,
    not visual.
  - Time-boxed at days, not weeks.
- Author **mid-fidelity wireframes** (per SOP §6.2.2):
  - Real content (no lorem ipsum), real labels, real
    navigation.
  - Annotations for interaction (hover, click, transitions).
  - Confirms flows work.
  - Begins incorporating component patterns from the design
    system.
  - The level at which usability testing produces useful
    signal.
- Author **high-fidelity wireframes** (per SOP §6.2.3):
  - Visual design applied (consumes art direction + tokens).
  - Confirms brand expression and visual hierarchy.
  - Includes responsive breakpoints (mobile / tablet /
    desktop minimum; sometimes wide-desktop).
  - Includes all interactive states (default, hover, active,
    focus, disabled, loading, error, success, empty) — these
    can reference per-component matrices rather than
    duplicating.
  - Annotated for engineering handoff (spacing, typography,
    motion).
- Refuse **lorem ipsum at mid-fi or hi-fi** (real content
  surfaces real problems; per SOP §6.7 anti-pattern).
- Refuse **single-breakpoint hi-fi** (mobile is where most
  users live; design mobile-first).
- Cite **art direction** + **design tokens** (for hi-fi) +
  **IA** (per `srs-author` §5.2) by stable name.
- Write to `docs/03-design/wireframes/<area>-{lo,mid,hi}.md`
  plus Figma file references.

## Handoffs to Other Skills

- **From `art-direction-author`** — visual language for hi-fi.
- **From `concept-author`** — narrative for any scrolly-tell
  / chaptered structure.
- **From `srs-author`** + IA work (Phase 2) — the structural
  spec wireframes implement.
- **From `design-tokens-author`** — tokens for hi-fi.
- **To `prototype-author`** — hi-fi wireframes feed clickable
  prototypes for usability testing.
- **To `usability-synthesis-author`** — usability test results
  surface wireframe issues; mid-fi typically gets re-revised.
- **To `component-states-matrix-author`** — wireframes
  reference matrices for interactive states; matrices grow as
  wireframes surface new components.
- **To `a11y-annotations-author`** — hi-fi wireframes are the
  surface for a11y annotations.
- **To `engineering-handoff-spec-author`** — hi-fi wireframes
  bundle into the handoff package.

## Edge Cases

- **Operator wants to skip lo-fi.** Refuse. Per SOP §6.7,
  skipping lo-fi means visual debate masks structural
  problems. Ship lo-fi even if a one-day version.
- **Operator wants to skip mid-fi and go from lo-fi to
  hi-fi.** Skipping mid-fi means usability testing waits
  for hi-fi (slower; more rework when issues surface).
  Surface the trade-off; allow only if the project is
  small enough that mid-fi and hi-fi would have been
  similar.
- **No real content available for mid-fi.** Halt; either
  partner with content lead to draft real content OR push
  back to Phase 2 to scope content production. Refuse
  lorem ipsum.
- **Hi-fi wireframe built only at desktop.** Refuse (per
  SOP §6.7 "designing only at one breakpoint"). Force
  mobile + tablet at minimum.
- **Wireframes diverge from IA mid-Phase 3.** Surface the
  divergence — either IA was wrong (re-enter Phase 2 IA
  work) OR wireframes are exceeding scope (cut back).
  Don't let wireframes silently redefine IA.
- **Operator wants production-grade detail at lo-fi.**
  Refuse the over-investment. Lo-fi's job is structure;
  more detail is wasted effort if structure changes.

## References

No external `references/*.md` files yet. The canonical
authorities are `internal://site-build-procedure.md` §6.2
(three fidelities) and `internal://docs/research/E2-agency-
methodologies.md` §C.4 (Hello Monday's 3-fidelity ladder).

## Self-Audit

Before declaring wireframes for a feature area shipped,
confirm:
- All three fidelities present (or explicit waiver with
  rationale for skipping mid-fi on small projects).
- No lorem ipsum at mid-fi or hi-fi.
- Hi-fi includes mobile + tablet + desktop (+ wide-desktop
  if applicable).
- Hi-fi includes interactive states (referencing component
  matrices).
- Art direction + tokens cited at hi-fi.
- IA / user flows cited at lo-fi.
- Lo-fi was reviewed for structure before mid-fi began.
