---
name: component-states-matrix-author
description: >
  Authors the per-component 9-state matrix —
  default / hover / focus / focus-visible / active / disabled /
  loading / error / empty / skeleton (often 9 or 10 depending on
  whether focus and focus-visible split). Each state has visual,
  behavior, and accessibility rows. Refuses to mark a component
  "ready" until every state is filled. Writes to
  docs/03-design/components/<component>.md (research/E3 §6.2;
  SOP §6.4.3). Use after design-tokens-author ships and per
  component as the design system grows. Do NOT use for: writing
  the full design system doc (use design-system-author Tier 3);
  generating design tokens (use design-tokens-author — states
  consume tokens); writing the engineering handoff spec (use
  engineering-handoff-spec-author — that is the bundle, not
  per-component); writing per-component motion (use motion-
  language-author for the language; per-component state
  transitions cite its tokens here).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C).
            Modeled on the user-invocable draft-component-states-
            matrix skill but conformed to meta-pipeline frontmatter
            / required-section discipline.
---

# component-states-matrix-author

Phase 3 — produce one component's 9-state matrix.

## When to Use

- A new component is being added to the design system; tokens
  exist; the matrix is the "design ready for engineering"
  contract.
- An existing component is being refactored or re-skinned and
  its state matrix needs re-authoring.
- A regression has surfaced an unhandled state (the missing
  empty state, the unspecified loading state) and the matrix
  needs to be filled.
- The product trio is reviewing whether a component is "ready"
  — the matrix is the readiness gate.

## When NOT to Use

- Tokens don't exist — `design-tokens-author` first. State
  matrices reference tokens by stable name; without them,
  this atom would invent values.
- Writing the full design-system doc — `design-system-author`
  (Tier 3). The matrix is per-component; the system
  encompasses Atomic Design hierarchy, content guidelines,
  maintenance, etc.
- Authoring tokens — `design-tokens-author`. States *consume*
  tokens; this atom doesn't define new ones.
- Writing the engineering-handoff spec — `engineering-handoff-
  spec-author`. The handoff bundles many matrices + tokens +
  motion + a11y; this atom produces one matrix.
- Writing the motion language — `motion-language-author`.
  State transitions cite motion tokens by name here; the
  language doc defines them.
- Per-component a11y annotations beyond what fits in the matrix
  — `a11y-annotations-author` (Tier 2) covers the deeper
  per-component a11y spec (semantic HTML, ARIA, keyboard, etc.).

## Capabilities Owned

- Author the matrix for one component with **9-10 states**:
  - **Default** — at-rest visual + behavior.
  - **Hover** — pointer hover; tooltip exposure if any.
  - **Focus** — keyboard focus (visible 2px outline at
    minimum).
  - **Focus-visible** — :focus-visible variant (focus from
    keyboard, not pointer; the modern best-practice split).
  - **Active** — pressed / pointer-down state.
  - **Disabled** — non-interactive; reduced opacity;
    `aria-disabled="true"`.
  - **Loading** — spinner / skeleton; `aria-busy="true"`.
  - **Error** — error styling + message; `aria-invalid="true"`.
  - **Empty** — no-data state with illustration / headline /
    primary CTA.
  - **Skeleton** — placeholder shape during data load
    (separate from full loading state).
- Per state, capture **three rows**:
  - **Visual** — what the user sees (cite token names, not
    hex values).
  - **Behavior** — what changes interactively (cite motion
    tokens for transitions).
  - **A11y** — semantic HTML / ARIA roles / keyboard /
    screen-reader announcements.
- Refuse "ready" status until **every state is filled**. No
  empty rows. The discipline is the deliverable.
- Cite **art direction** + **motion language** + **design
  tokens** by stable name.
- Cross-reference to **a11y-annotations-author** (Tier 2) for
  the deeper a11y spec when the matrix's a11y row points to
  it.
- Write to `docs/03-design/components/<component>.md`.

## Handoffs to Other Skills

- **From `art-direction-author`** — visual stance per state
  draws from art direction's palette + type.
- **From `motion-language-author`** — state transitions
  reference motion tokens.
- **From `design-tokens-author`** — visual rows cite tokens.
- **To `a11y-annotations-author`** (Tier 2) — deeper a11y
  spec lives there; matrix's a11y rows summarize.
- **To `engineering-handoff-spec-author`** — matrices bundle
  into the handoff package.
- **To Storybook stories** — each state becomes a story
  (`Component.stories.tsx` per state); matrix is the spec
  the stories implement.
- **From the user-invocable `draft-component-states-matrix`** —
  peer skill producing the same artifact via a different
  procedure.

## Edge Cases

- **Component is non-interactive** (e.g., a static logo). Many
  states collapse: default + (optionally) skeleton. Document
  explicitly that hover/focus/active/disabled are N/A; don't
  fabricate empty rows.
- **Component is decorative motion only** (e.g., a hero
  particle effect). Even more states collapse; the matrix
  becomes default + reduced-motion. Mark non-applicable
  states explicitly.
- **Loading vs Skeleton overlap.** They're related but
  distinct: loading is the user-initiated state (button
  pressed; data fetching); skeleton is the placeholder
  during async render. Per-component, decide which applies;
  often both, in sequence.
- **Empty state with no design.** Common dysfunction. Refuse
  to ship the matrix without an empty state designed (per
  SOP §6.7 anti-pattern "states not designed"). Push back to
  art direction if needed.
- **State requires a designed illustration** (empty state
  often does). Note the dependency; the matrix can be
  authored with a placeholder + dependency, but the
  component isn't "ready" until the illustration exists.
- **Component variants** (button-primary / button-secondary /
  button-ghost). Author one matrix per variant OR a shared
  matrix with variant column; pick based on state-divergence
  across variants.

## References

No external `references/*.md` files yet. The canonical
authorities are `internal://docs/research/E3-technical-conventions.md`
§6.2 (9-state matrix discipline + Carbon / Material / Pajamas
references) and the SOP §6.4.3. The user-invocable
`draft-component-states-matrix` is a peer skill producing the
same artifact via a different procedure.

## Self-Audit

Before declaring a component matrix complete, confirm:
- All 9-10 states present (or explicitly marked N/A with
  rationale).
- Each state has visual / behavior / a11y rows filled.
- Visual rows cite tokens by name (no hex values).
- Behavior rows cite motion tokens for transitions.
- A11y rows include semantic HTML + keyboard + ARIA.
- Empty state has illustration + headline + primary CTA OR
  documented dependency on illustration.
- Cross-reference to `a11y-annotations-author` if deeper
  a11y spec is needed.
- Stories file (or design-tool equivalent) referenced.
