---
name: design-system-author
description: >
  Authors the project's full Design System documentation — Atomic
  Design hierarchy (atoms / molecules / organisms / templates /
  pages), per-component owner + version + deprecation policy,
  contribution model, content guidelines, internationalization
  considerations, and Storybook-or-equivalent live documentation
  pointer. Bundles design-tokens-author + component-states-matrix-
  author + a11y-annotations-author into the system layer that
  governs maintenance. Writes to docs/03-design/design-system.md
  (SOP §6.4 full). Use after ≥3 templates exist AND tokens +
  states + a11y annotations are in place. Do NOT use for:
  generating design tokens (use design-tokens-author); writing
  per-component state matrices (use component-states-matrix-
  author); writing per-component a11y annotations (use
  a11y-annotations-author); writing the engineering handoff (use
  engineering-handoff-spec-author); designing wireframes (use
  wireframe-author).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C).
---

# design-system-author

Phase 3 — produce the full Design System documentation.

## When to Use

- Project has ≥3 templates AND tokens + state matrices +
  a11y annotations exist; the system layer is the next
  step that turns piece-parts into a maintainable whole.
- A multi-property project (marketing site + product app)
  needs a unified design system with per-property variants.
- A re-platform / re-brand is taking the existing system in
  a new direction; the system doc is being re-authored.
- An audit reveals that piece-parts (tokens, components)
  exist but the maintenance discipline (versioning, owner,
  contribution model) doesn't — author it.

## When NOT to Use

- Per SOP §6.4: "If the site has more than a handful of
  templates, formalize the design system rather than producing
  one-off page designs." For single-template sites or
  microsites, the system is overkill — skip this atom; ship
  tokens + matrices + annotations only.
- Generating design tokens — `design-tokens-author`. Tokens
  are one input to the system.
- Writing per-component state matrices — `component-states-
  matrix-author`. Matrices are inputs.
- Writing per-component a11y annotations —
  `a11y-annotations-author`. Annotations are inputs.
- Writing the engineering handoff spec —
  `engineering-handoff-spec-author`. The handoff is the
  contract; the system is the *content* the contract
  references.
- Writing wireframes — `wireframe-author`. Wireframes apply
  the system; they're not the system.
- Producing Storybook stories themselves — engineering
  concern. This atom *references* Storybook as the live doc
  layer; doesn't author the stories.

## Capabilities Owned

- Document the **Atomic Design hierarchy** per SOP §6.4.2:
  - **Atoms** — buttons, inputs, labels, icons, single-
    purpose primitives.
  - **Molecules** — input-with-label, search-bar, breadcrumb
    item, navigation link.
  - **Organisms** — navigation bar, footer, hero, card, form.
  - **Templates** — page layouts (organisms in arrangement).
  - **Pages** — specific instances with real content.
- Per component, capture **maintenance discipline**:
  - **Owner** — named individual or role accountable.
  - **Version** — semantic versioning of the component
    (MAJOR for breaking, MINOR for additive, PATCH for
    fixes).
  - **Deprecation policy** — how a component is retired
    (deprecation banner; migration path; sunset date).
  - **Contribution model** — how new components or changes
    enter the system (PR review, design review, sign-off
    chain).
- Document **content guidelines** per SOP §6.4.6:
  - Voice and tone (consume `concept-author`'s voice).
  - Microcopy patterns (button labels, error messages,
    empty states).
  - Length constraints.
  - Internationalization (text expansion in other
    languages — German often 30%+ longer; RTL languages).
- Reference **Storybook** (or Ladle / Histoire) as the live
  documentation layer. Per SOP §6.4.7 the system is a living
  artifact; Storybook is the working surface.
- Document the **system's relationship to the broader
  family**:
  - Cite `art-direction-author` as the visual stance.
  - Cite `design-tokens-author` as the encoded values.
  - Cite `component-states-matrix-author` (collected) as
    the per-component spec.
  - Cite `a11y-annotations-author` (collected) as the
    a11y posture.
  - Cite `motion-language-author` as the motion contract.
- Write to `docs/03-design/design-system.md`.

## Handoffs to Other Skills

- **From all Tier 1 atoms in this family** — tokens,
  matrices, motion, a11y, art direction, concept.
- **From `wireframe-author`** — wireframes inform what
  components need to exist in the system.
- **From `usability-synthesis-author`** — usability
  findings often surface system gaps (missing component,
  inconsistent pattern).
- **To `engineering-handoff-spec-author`** — the system is
  the bundle the handoff references.
- **To Phase 4 build** — engineering implements components
  per the system's spec.
- **To Phase 7 maintenance** — the system is a living
  artifact; updates flow continuously.

## Edge Cases

- **Single-template site** (microsite, campaign page).
  System overkill; refuse and recommend tokens + matrices +
  annotations alone.
- **Multi-property project** with conflicting design
  intents. Author a parent system + per-property
  variants; refuse a single mega-system that papers over
  conflict.
- **Storybook doesn't exist yet.** Recommend it as a
  Phase 4 Sprint-0 deliverable; the system doc references
  components against design-tool sources meanwhile.
- **Operator wants to add components without going
  through the contribution model.** Refuse silent
  additions; the system loses integrity. The contribution
  model is the discipline; surface drift in the Stage 6
  family audit.
- **Component is third-party** (e.g., Radix UI primitive).
  Document the third party's role; the system documents
  *our* wrapper / theming, not the third party itself.
- **Versioning conflict** — designer ships v2 of a
  component but engineering still uses v1 in production.
  Document deprecation timeline; the system tracks both
  versions until v1 is fully migrated.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §6.4
(full design-system section).

## Self-Audit

Before declaring a design system doc complete, confirm:
- Atomic Design hierarchy populated (atoms → pages).
- Per-component: owner + version + deprecation policy.
- Contribution model documented.
- Content guidelines (voice, tone, microcopy patterns).
- Internationalization considerations stated.
- Storybook (or equivalent) referenced as live doc layer.
- Cross-references to art direction, tokens, matrices,
  a11y annotations, motion language by stable name.
- System acknowledges its living-artifact nature
  (versioning + maintenance cadence).
