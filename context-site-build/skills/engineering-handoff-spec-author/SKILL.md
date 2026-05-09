---
name: engineering-handoff-spec-author
description: >
  Authors the Engineering Handoff Spec — the contract from Design
  to Engineering at Phase 3 close. Bundles the design system
  (tokens + component matrices), per-component a11y requirements,
  motion specs, the Figma file structure, and the design QA
  contact. Refuses "throw it over the wall" hand-offs (requires
  product-trio model evidence). Writes to
  docs/03-design/engineering-handoff/<area>.md (research/E3 §6.6;
  SOP §6.6). Use at end of Phase 3 Design, before Phase 4 sprint
  planning. Do NOT use for: generating design tokens (use
  design-tokens-author — that is one input); writing per-component
  state matrices (use component-states-matrix-author); writing
  motion specs (use motion-language-author); writing per-component
  a11y annotations (use a11y-annotations-author Tier 2); writing
  the SRS (use srs-author — that is the spec for what gets built;
  this is the spec for how it looks + behaves).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C).
            Modeled on the user-invocable draft-handoff-spec
            skill but conformed to meta-pipeline frontmatter /
            required-section discipline.
---

# engineering-handoff-spec-author

Phase 3 close — produce the Engineering Handoff Spec for one
deliverable area.

## When to Use

- Phase 3 Design is closing; tokens + component matrices +
  motion language + a11y annotations exist; the handoff is the
  Gate 3 final deliverable.
- A new feature area's design is complete and engineering
  needs the contract before Sprint 0.
- A re-skin / refactor is shipping and engineering needs the
  delta documented as a focused handoff.
- A design QA dispute has surfaced ("engineering says the
  design is unimplementable; design says engineering misread")
  — re-author the handoff to clarify.

## When NOT to Use

- Tokens, matrices, motion, or a11y annotations don't exist —
  those are the upstream inputs. The handoff bundles them; it
  doesn't replace them.
- Authoring tokens — `design-tokens-author`.
- Writing per-component state matrices —
  `component-states-matrix-author`.
- Writing motion specs — `motion-language-author`.
- Writing per-component a11y annotations beyond bundling —
  `a11y-annotations-author` (Tier 2).
- Writing the SRS — `srs-author` (site-build family). The SRS
  is *what* gets built; the handoff is *how it looks +
  behaves*. Both reference each other.
- Implementing the design — that's Phase 4 build, not Phase 3
  handoff.
- Sprint planning — Phase 4 ceremony, downstream of this.

## Capabilities Owned

- Bundle the **design-system inputs** by reference, not by
  copy:
  - Token system (`design-tokens-author` output).
  - Per-component matrices (`component-states-matrix-author`
    outputs for every component in the deliverable area).
  - Motion language (`motion-language-author` output).
  - A11y annotations (`a11y-annotations-author` Tier 2 outputs).
- Document the **Figma file structure** — pages, components
  organization, naming conventions, version-pinning policy
  for the Figma file (engineering shouldn't be reading a
  moving target).
- Capture **per-component spec pages** in Storybook (or
  equivalent). Each component has a story per state plus
  documentation. Storybook is the live design-engineering
  contract per E3 §6.6.
- Document **animation specs** — easing, duration, properties
  animated, with motion-token references.
- Name the **design QA contact** — the designer engineering
  can ask. Phase 4 isn't a clean break; iterative design
  questions need an owner.
- Refuse the **"throw it over the wall" hand-off** — require
  evidence that the product trio (PdM + Tech Lead + Lead
  Designer) operated through Phase 3. Without it, surface
  the §6.6 dysfunction explicitly.
- Cite all **upstream artifacts** by stable name + path.
- Write to `docs/03-design/engineering-handoff/<area>.md`.

## Handoffs to Other Skills

- **From every Tier 1 / Tier 2 atom in this family** — the
  handoff bundles them.
- **From `art-direction-author`** — handoff includes the art
  direction by reference.
- **From `concept-author`** — handoff includes the concept
  by reference (engineers benefit from understanding the
  creative thesis they're implementing).
- **To `srs-author`** (site-build family) — the SRS
  references handoff areas; the two are siblings, not
  upstream/downstream.
- **To Phase 4 build** — engineering consumes this as the
  contract.
- **To `prototype-author`** (Tier 2) — clickable prototype
  may be part of the handoff bundle.
- **From the user-invocable `draft-handoff-spec`** — peer
  skill producing the same artifact via a different
  procedure.

## Edge Cases

- **Tokens or matrices are incomplete.** Halt; the handoff
  is a bundle of complete artifacts. An incomplete bundle
  ships incomplete state matrices, which surface as
  Phase 4 Sprint-0 dysfunction.
- **Product trio model not in place.** Surface explicitly;
  ship the handoff with a banner noting the §6.6
  dysfunction risk + recommend a Phase 4 retro to
  reconfigure the team.
- **Multi-area handoff** (the whole design system, not just
  one feature area). Split by area; one handoff doc per
  feature area. Refuse a single mega-handoff that
  engineering can't read end-to-end.
- **Storybook doesn't exist.** Recommend it (per E3 §6.4)
  as a Phase 4 Sprint-0 deliverable; the handoff doc
  documents the components against design-tool sources
  meanwhile, with Storybook conversion as a tracked
  follow-up.
- **Design changes mid-build.** Re-author the handoff for
  the changed components; the original handoff is
  archived. Don't patch silently — the contract was the
  hand-off; changes need to be visible.

## References

No external `references/*.md` files yet. The canonical
authorities are `internal://docs/research/E3-technical-conventions.md`
§6.6 (design-to-dev handoff chain: Figma + Tokens Studio +
Style Dictionary + Storybook + Chromatic) and the SOP §6.6.
The user-invocable `draft-handoff-spec` is a peer skill
producing the same artifact via a different procedure.

## Self-Audit

Before declaring an engineering-handoff spec complete,
confirm:
- All upstream artifacts cited by stable name + path
  (tokens, matrices, motion, a11y).
- Figma file structure documented (pages + naming +
  version-pin policy).
- Storybook (or equivalent) referenced for live spec.
- Animation specs reference motion tokens by name.
- Design QA contact named.
- Product-trio evidence captured OR §6.6 dysfunction
  flagged.
- Per feature area, not mega-bundle.
- Handoff is ≤6 pages rendered (deeper specs live in the
  cited artifacts).
