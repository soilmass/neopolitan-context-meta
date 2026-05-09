---
name: design-philosophy-author
description: >
  Authors the project's one-page Design Philosophy — brand
  expression goals, audience attributes, tone (visual feel),
  constraints (a11y floor, performance budget), inspirations with
  critique of why they work, and anti-references (patterns to
  deliberately avoid). Anchors design reviews and prevents design-
  by-stakeholder-preference. Writes to docs/03-design/design-philosophy.md
  (site-build-procedure.md §6.1). Use at the start of Phase 3
  Design, before wireframes. Do NOT use for: authoring the project
  vision (use vision-author — vision is business-outcome focused;
  design philosophy is visual / experiential focused); persona
  authoring (use persona-author); generating design tokens (Phase
  3 sub-deliverable; out of scope here); writing the SRS (use
  srs-author); writing the engineering handoff spec (Phase 3
  sub-deliverable; out of scope here).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.2.0
            Tier 2/3 expansion pass. Modeled on the user-invocable
            draft-design-philosophy skill but conformed to
            meta-pipeline frontmatter / required-section discipline.
---

# design-philosophy-author

Phase 3 — produce the project's one-page design philosophy.

## When to Use

- Phase 3 Design begins; vision, personas, and KPIs exist; the
  Phase 2 architecture is locked; the design lead is starting
  the design-philosophy doc before wireframes.
- A major rebrand or visual-direction pivot has occurred and
  the existing philosophy no longer matches the work.
- A design review has surfaced "we have no shared frame of
  reference" — the philosophy is the frame.
- A new design lead has joined and needs to absorb-or-evolve
  the existing direction.

## When NOT to Use

- **Vision authoring** — `vision-author`. The vision is
  business-outcome focused (target user × problem × outcome);
  the design philosophy is visual and experiential focused
  (brand expression × tone × constraints). Both exist and
  cross-reference.
- Persona authoring — `persona-author`. Personas inform the
  philosophy's "audience attributes" but the persona docs are
  upstream.
- Generating design tokens (Phase 3 sub-deliverable). The
  philosophy informs token decisions; the token spec is its
  own artifact (deferred to a future `site-design` family).
- Writing the SRS — `srs-author`. The philosophy is design-
  intent; SRS is functional + non-functional requirements.
- Engineering handoff spec — Phase 3 sub-deliverable, out of
  scope here. Handoff is the contract from design to
  engineering; philosophy is the design's compass.
- Stack-specific styling decisions (Tailwind config, CSS
  architecture). Those follow from the philosophy but live
  in code.

## Capabilities Owned

- Author the **brand expression goals** per SOP §6.1 — how
  does the design reinforce the brand? Which brand attributes
  surface where (hero vs detail; copy vs imagery; motion vs
  stillness)?
- Document **audience attributes** — who's the user, how do
  they engage with similar products, what conventions do they
  expect (e-commerce vs B2B SaaS vs editorial vs portfolio).
- Capture **tone** — voice and visual feel (energetic /
  minimal / trustworthy / playful / authoritative / warm /
  technical). One sentence per tone facet.
- Document **constraints** — accessibility floor (WCAG 2.2
  AA per SOP §5.1.2), performance budget impact (motion-
  heavy vs static), brand guidelines (logo usage, color
  reservations, typography licensing).
- Curate **inspirations** with critique — references (named
  agencies, sites, products) WITH a written critique of why
  they work. References without critique are mood-board
  noise; this atom requires the why.
- Curate **anti-references** — patterns to deliberately
  avoid. Often more decisive than inspirations: naming what
  the design will NOT be cuts more design-by-committee
  conflicts than naming what it will be.
- Produce a **one-page** artifact (the SOP discipline; longer
  is design system territory). Refuses to ship a multi-page
  philosophy.
- Write to `docs/03-design/design-philosophy.md`.

## Handoffs to Other Skills

- **From `vision-author`** — vision's brand differentiation
  feeds brand expression goals.
- **From `persona-author`** — personas feed audience
  attributes.
- **From `kpi-author`** — KPIs constrain the philosophy
  (e.g., conversion-rate KPI shapes friction tolerance in the
  visual hierarchy).
- **To Phase 3 sub-deliverables** — wireframes, design
  tokens, design system, prototype usability testing, all
  governed by this philosophy.
- **To `srs-author`** — non-functional requirements
  reference the philosophy's accessibility and performance
  constraints.
- **To design reviews** — the philosophy anchors review
  conversations; refuses subjective "I like it" critiques in
  favor of "does this match the philosophy" tests.
- **From the user-invocable `draft-design-philosophy`** —
  peer skill.

## Edge Cases

- **No vision / no personas yet.** Halt; the philosophy needs
  upstream context. Don't start Phase 3 work without Phase 1
  outputs.
- **Conflicting brand-team direction** — sponsor wants
  "trustworthy and minimal"; brand team wants "playful and
  bold." Surface the conflict in the philosophy explicitly;
  refuse to ship a synthesized "minimal-yet-bold" that
  papers over the disagreement. The Sponsor resolves.
- **Inspirations list with no critique.** Refuse; the why is
  the load-bearing part. References without critique become
  pinterest mood boards.
- **Anti-references absent.** Push hard for ≥3. "What we
  will not be" is a faster path to consensus than "what we
  will be."
- **Multi-page philosophy.** Refuse; collapse to one page.
  If detail is needed, push it into design-system docs
  (deferred Phase 3 sub-deliverable).

## References

No external `references/*.md` files yet — first real
authoring run will produce a template worth promoting. The
canonical authority is `internal://site-build-procedure.md`
§6.1. The user-invocable `draft-design-philosophy` is a peer
skill producing the same artifact via a different procedure.

## Self-Audit

Before declaring a design philosophy complete, confirm:
- One page rendered (≤500 words is a useful proxy).
- Brand expression goals named explicitly (≥3 attributes).
- Audience attributes link to ≥1 persona by stable handle.
- Tone is captured in ≥3 voice + visual facets.
- ≥3 inspirations, each with a written critique of why it
  works.
- ≥3 anti-references explicitly named.
- Constraints include a11y floor (WCAG 2.2 AA) and
  performance budget posture (motion-heavy / motion-light /
  static).
