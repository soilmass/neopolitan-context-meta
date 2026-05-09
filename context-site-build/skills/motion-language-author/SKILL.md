---
name: motion-language-author
description: >
  Authors the project's Motion Language document — durations,
  easings, choreography rules, motion tokens, per-interaction
  motion contracts, prefers-reduced-motion policy, and the
  taxonomy of expressive vs productive motion. Operationalizes
  the art direction's motion vocabulary and the concept's
  narrative purpose of motion into rules an engineer implements
  against. Writes to docs/03-design/motion-language.md
  (research/E3 §6.3; SOP §6.4.1 motion tokens partial). Use after
  art-direction-author and concept-author have produced their
  artefacts. Do NOT use for: authoring the visual language (use
  art-direction-author); authoring the creative thesis (use
  concept-author); generating full design tokens (use
  design-tokens-author — motion tokens are a category of those);
  authoring per-component state matrices (use
  component-states-matrix-author); authoring the prefers-reduced-
  motion CSS implementation (engineering concern, downstream).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C). No
            user-invocable peer exists for this Awwwards-tier
            addition; this atom establishes the pattern.
---

# motion-language-author

Phase 3 — produce the project's Motion Language document.

## When to Use

- Phase 3 Design is in progress; art direction + concept have
  shipped; the motion language is the next deliverable that
  governs every animated interaction in the project.
- An Awwwards-tier project where Animations/Transitions is the
  highest-leverage developer-award sub-score (per E1 research,
  mean 8.7/10 on SOTY winners) and the motion deserves its own
  spec.
- Motion specs across multiple components are starting to
  diverge ("each developer is making their own easing curves")
  and a unified language is needed.
- A motion-heavy redesign / rebrand and the existing motion
  language no longer matches.

## When NOT to Use

- Art direction or concept don't exist — those are
  prerequisites. Motion language operationalizes the upstream
  creative direction; without them, this atom is producing
  arbitrary timings.
- Authoring the visual language — `art-direction-author`
  states the motion *vocabulary* (cinematic / restrained /
  energetic / playful); motion-language-author operationalizes
  it into tokens + rules.
- Authoring the concept — `concept-author` states the
  *narrative purpose* of motion (lead / accent / recede);
  motion-language-author operationalizes it into per-
  interaction contracts.
- Generating the full design tokens — `design-tokens-author`
  consumes motion tokens defined here as one category of the
  full token system.
- Writing per-component motion specs — those live in
  `component-states-matrix-author`'s state-transition rows.
- Implementing `prefers-reduced-motion` CSS — engineering
  concern. This atom defines the policy (hard-disable / soft-
  degrade / alternative experience per E3 §4.2); engineering
  implements it.

## Capabilities Owned

- Define **motion principles** — the project's motion
  philosophy in one paragraph (often paired with the IBM
  Carbon expressive-vs-productive taxonomy or Material's
  informative/focused/expressive × hierarchy/feedback/status
  taxonomy).
- Author the **motion tokens**:
  - **Duration tokens** — `motion-duration-fast` (~150ms),
    `motion-duration-medium` (~250-400ms),
    `motion-duration-slow` (~600-1000ms), plus an `instant`
    bucket (~50-100ms).
  - **Easing tokens** — `motion-ease-in`, `motion-ease-out`,
    `motion-ease-in-out`, plus project-specific easings
    (e.g., a custom cubic-bezier for the brand's signature
    movement quality).
  - Tokens follow the `{prefix}-motion-{property}-{modifier}`
    naming (per E3 §6.3 IBM/Material model).
- Define **choreography rules** — when motion *leads* the
  story (scroll-driven narrative; hero animation), when it
  *accents* (page transitions; hover feedback), when it
  *recedes* (functional motion only — modals, tooltips).
- Author **per-interaction motion contracts** for the project's
  most-used patterns (page enter, scroll-section reveal,
  modal open, hover, drag, error shake, success confirmation).
  Each contract names the duration token + easing token +
  property animated.
- Document **`prefers-reduced-motion` policy** — pick one of
  the three flavors per E3 §4.2 (hard-disable / soft-degrade /
  alternative experience) and state the rationale. The opt-in
  pattern (base CSS without motion; motion inside `@media
  (prefers-reduced-motion: no-preference)`) is the default.
- State the **performance budget** for motion — 60fps target
  on which devices, when scroll-driven motion is acceptable,
  whether WebGL motion is in scope (cite art direction's
  motion vocabulary).
- Cite **art direction** + **concept** by stable name.
- Write to `docs/03-design/motion-language.md`.

## Handoffs to Other Skills

- **From `art-direction-author`** — motion vocabulary stated
  there gets operationalized.
- **From `concept-author`** — narrative purpose of motion
  (lead / accent / recede) gets operationalized.
- **To `design-tokens-author`** — motion tokens defined here
  feed the broader DTCG token system.
- **To `component-states-matrix-author`** — state transitions
  reference motion tokens by stable name.
- **To `concept-prototyping-author`** (Tier 2) — concept
  prototypes test motion-language assumptions in 3D / runtime
  tools.
- **To `engineering-handoff-spec-author`** — motion-language
  doc is part of the handoff package.

## Edge Cases

- **Motion-light project** (functional only). Acceptable;
  document the stance and define a minimal token set
  (functional durations + ease-out only). Per the SOP §6.4.1
  motion is a token category whether the project is motion-
  heavy or motion-light.
- **Stakeholder demands every interaction be animated.**
  Refuse silent acquiescence; surface the perf cost (per E3
  §1.1 INP is the Achilles heel of motion-heavy sites at
  300-500ms on mid-range Android). Force a discipline of
  *purposeful* motion vs decorative motion.
- **No `prefers-reduced-motion` policy in the existing
  product.** This atom requires one. Default to the opt-in
  pattern + add a UI toggle (per E3 §4.2 Smashing's
  recommendation).
- **Motion conflicts with the art direction's vocabulary**
  (art direction says "restrained"; concept says "scroll-
  driven cinematic"). Halt; the upstream contradiction
  surfaces here. Either re-enter art direction OR concept
  to resolve.
- **Per-interaction contracts diverge from project's existing
  components.** Document the deltas explicitly; the
  motion-language doc supersedes ad-hoc per-component
  motion. Migration path: re-spec divergent components in
  `component-states-matrix-author` next.

## References

No external `references/*.md` files yet. The canonical
authorities are `internal://docs/research/E3-technical-conventions.md`
§6.3 (motion specs taxonomy + tooling) plus the SOP §6.4.1
motion-token category. The IBM Carbon expressive-vs-productive
and Material informative/focused/expressive × hierarchy/feedback/
status/character taxonomies are the named industry references.
No user-invocable peer exists for this Awwwards-tier addition.

## Self-Audit

Before declaring a motion-language doc complete, confirm:
- Motion principles stated in one paragraph (cite IBM/Material
  taxonomy if used).
- Duration tokens span ≥4 buckets (instant / fast / medium /
  slow).
- Easing tokens cover ≥3 standard curves (ease-in, ease-out,
  ease-in-out) + any project-specific ones.
- Choreography rules name when motion leads / accents /
  recedes.
- Per-interaction contracts cover ≥6 of the most-used
  patterns (page enter, scroll-reveal, modal, hover, drag,
  error, success).
- `prefers-reduced-motion` policy declared (hard-disable /
  soft-degrade / alternative experience).
- Performance budget for motion stated (60fps target +
  device tier).
- Art direction + concept cited by stable name.
- Doc is ≤4 pages rendered.
