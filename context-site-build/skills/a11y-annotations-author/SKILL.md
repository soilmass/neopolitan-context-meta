---
name: a11y-annotations-author
description: >
  Authors per-component accessibility annotations on hi-fi designs —
  semantic HTML element to use, ARIA roles / properties / states,
  keyboard interaction (Tab order, Enter / Space behaviors,
  arrow-key behaviors), focus management, screen-reader
  announcements, color contrast verification (4.5:1 normal text;
  3:1 large text + UI controls), touch target size (44×44 px
  minimum), motion preferences. Writes to
  docs/03-design/a11y-annotations/<component>.md (SOP §6.4.5).
  Use during or after hi-fi wireframes ship and per component as
  the design system grows. Do NOT use for: writing the WCAG
  conformance statement (out of scope here; that's a Phase 5
  hardening artifact in the site-build family or future
  site-operate); per-component state matrices (use
  component-states-matrix-author — that bundles a summary a11y
  row; this atom does the deep spec); writing motion specs (use
  motion-language-author); a11y audit (Phase 5 deliverable);
  remediation of existing production a11y issues (different
  workflow, post-launch).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C).
---

# a11y-annotations-author

Phase 3 — produce per-component accessibility annotations.

## When to Use

- Phase 3 Design is in progress; hi-fi wireframes ship; the
  per-component a11y annotations are the design's promise to
  engineering for what accessibility looks like.
- A new component is being added to the design system; the
  state matrix exists; the a11y annotations deepen the
  matrix's a11y row.
- An a11y review (per SOP §6.8 Gate 3 criterion "A11y
  annotations reviewed by Accessibility Specialist") needs
  the annotations as input.
- A regression has surfaced an unhandled a11y case (focus
  order broken, ARIA role missing) and the annotations need
  re-authoring.

## When NOT to Use

- Hi-fi wireframes don't exist — `wireframe-author` first.
  Annotating non-existent designs is fiction.
- Writing the WCAG conformance statement — that's a Phase 5
  hardening artifact in the site-build family (or a future
  site-operate family). Annotations are design-time;
  conformance is post-implementation.
- Per-component state matrices — `component-states-matrix-
  author`. The matrix bundles a summary a11y row; this atom
  produces the deep spec the matrix's row points to.
- Motion specs — `motion-language-author`. Motion
  preferences (`prefers-reduced-motion`) policy lives in
  motion language; per-component motion compliance lives in
  this atom's annotations.
- A11y audit — Phase 5 deliverable. Audit *measures*
  conformance; annotations *specify* the design intent.
- Remediation of existing production a11y issues — different
  workflow, different pacing, post-launch concern.

## Capabilities Owned

- Author per-component a11y annotations per SOP §6.4.5:
  - **Semantic HTML element to use** — `<button>` not
    `<div>`; `<nav>` for navigation; `<dialog>` for modals;
    landmark roles where appropriate.
  - **ARIA roles, properties, states** — only when semantic
    HTML alone is insufficient (per WCAG 1st Rule of ARIA:
    don't use ARIA when semantic HTML works).
  - **Keyboard interaction** — Tab order, Enter / Space
    behaviors, arrow-key behaviors for grouped controls
    (radio groups, tab lists, menus).
  - **Focus management** — where focus moves on action
    (modals trap focus; closing modals returns focus;
    page transitions announce the new page).
  - **Screen-reader announcements** — live regions for
    status updates, polite vs assertive `aria-live`,
    `aria-label` / `aria-describedby` patterns.
  - **Color contrast verified** — 4.5:1 for normal text;
    3:1 for large text + UI controls; tools (Stark,
    Contrast app, axe).
  - **Touch target size** — 44×44 px minimum (mobile +
    tablet); document where this exceeds the visual size
    via padded hit area.
  - **Motion preferences** — respects `prefers-reduced-
    motion`, citing the policy from
    `motion-language-author`.
- Document **WCAG 2.2 success criteria** the component
  maps to (e.g., 2.1.1 Keyboard, 2.4.7 Focus Visible, 1.4.3
  Contrast, 2.5.8 Target Size).
- Cite **art direction** (focus indicators per art
  direction's contrast palette), **motion language**
  (reduced-motion policy), **component states matrix** (the
  a11y row this atom deepens) by stable name.
- Write to `docs/03-design/a11y-annotations/<component>.md`.

## Handoffs to Other Skills

- **From `wireframe-author`** — hi-fi wireframes are the
  surface annotations live on.
- **From `component-states-matrix-author`** — state matrix's
  a11y row points to this atom's deeper spec.
- **From `motion-language-author`** — `prefers-reduced-
  motion` policy.
- **From `art-direction-author`** — focus indicator
  styling.
- **To `engineering-handoff-spec-author`** — annotations
  bundle into the handoff package.
- **To Phase 4 build** — engineering implements per
  annotations.
- **To Phase 5 hardening** — a11y conformance statement
  references the annotations as the design intent that
  hardening verifies.

## Edge Cases

- **Designer / engineer disagree on the right semantic
  element.** Convene; the WCAG 1st Rule of ARIA breaks
  most ties (use native HTML; reach for ARIA only when
  necessary). Document the decision in the annotation.
- **Custom cursor present.** Per E3 §4.4, custom cursors
  routinely break 2.4.7 Focus Visible. The annotations
  must document focus-visible parity (focus-ring shows
  when the custom cursor is active OR custom cursor
  changes for keyboard focus).
- **Decorative `<canvas>` (WebGL hero).** Add
  `aria-hidden="true"` to the canvas; ensure the page has
  an equivalent text alternative for screen readers (text
  hero behind the canvas).
- **Drag-only interaction.** Per WCAG 2.5.7 (new in 2.2),
  drag must have a single-pointer alternative. The
  annotation documents the alternative (click-to-select +
  click-to-place; or keyboard via arrow keys).
- **Component is a third-party widget** (e.g., a
  third-party video player). Document the third party's
  a11y posture; if it falls short, document the
  workaround (e.g., custom controls overlay) or escalate
  to risk register.
- **Operator wants to defer a11y annotations to Phase 5.**
  Refuse per SOP §6.7 anti-pattern: "Color contrast and
  a11y as a Phase 5 audit. Designing in compliance is
  cheaper than retrofitting." Annotations are Phase 3
  work.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §6.4.5
plus `internal://docs/research/E3-technical-conventions.md`
§4 (accessibility on motion-heavy sites). WCAG 2.2 success
criteria are the named industry standard.

## Self-Audit

Before declaring a component's a11y annotations complete,
confirm:
- Semantic HTML element specified (with rationale if
  ARIA is used).
- Keyboard interaction documented (Tab order, key
  behaviors).
- Focus management documented (where focus moves on
  action).
- Screen-reader announcements documented (live regions,
  aria-label patterns).
- Color contrast verified at 4.5:1 / 3:1 (with tool
  cited).
- Touch target ≥44×44 px (or padded hit area documented).
- `prefers-reduced-motion` compliance noted (citing
  motion-language policy).
- WCAG 2.2 success criteria mapped.
- Art direction + motion language + state matrix cited
  by stable name.
