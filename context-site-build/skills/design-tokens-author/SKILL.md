---
name: design-tokens-author
description: >
  Authors the project's design-token system — DTCG JSON as source
  of truth piped through Style Dictionary v4 to CSS variables,
  Tailwind v4 @theme, and TypeScript types. Token categories cover
  color (palette + scale), typography (families + scale), spacing,
  radius, shadow / elevation, motion (consumes motion-language-
  author's tokens), z-index, breakpoints. Includes a CI gate that
  fails the build if tokens.json is edited without regenerating
  outputs. Writes to design-tokens/{tokens.json, build-tokens.config.ts}
  and the generated CSS / TS / Tailwind outputs (research/E3 §6.1;
  SOP §6.4.1). Use after art-direction-author + motion-language-
  author ship. Do NOT use for: authoring the visual language (use
  art-direction-author — that is the human-readable contract);
  authoring motion specs (use motion-language-author); per-component
  state styling (use component-states-matrix-author); writing the
  full design system doc (use design-system-author Tier 3).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.3.0
            site-design family bootstrap (Phase 2 of Option C).
            Modeled on the user-invocable draft-design-system-tokens
            skill but conformed to meta-pipeline frontmatter /
            required-section discipline.
---

# design-tokens-author

Phase 3 — produce the project's design-token system.

## When to Use

- Phase 3 Design is in progress; art direction + motion language
  have shipped; the token system is the bridge between design
  intent and code.
- A new project bootstrapping its design system needs token-
  scaffolding before component work begins.
- A migration to W3C DTCG-format tokens (per the Oct 2025 stable
  spec) from an ad-hoc Tailwind config or hex-littered code.
- A multi-property / multi-brand project needing per-brand token
  themes that share a common scale.

## When NOT to Use

- Art direction or motion language don't exist — they're the
  upstream sources of truth. Tokens encode them; without them,
  this atom would be inventing values.
- Authoring the visual language — `art-direction-author`. Tokens
  are the *code-side expression*; art direction is the
  human-readable contract.
- Authoring motion-token semantics — `motion-language-author`
  defines the buckets (fast / medium / slow) and rationale; this
  atom encodes them as DTCG tokens.
- Per-component state styling — `component-states-matrix-author`.
  States *consume* tokens; the matrix is per-component.
- Writing the full design system doc — `design-system-author`
  (Tier 3). Tokens are one input; the system encompasses much
  more (Atomic Design hierarchy, content guidelines, maintenance
  policy).
- Hand-coding `tailwind.config.ts` with hex values — anti-pattern
  per E3 §6.6. Tokens flow through Style Dictionary; Tailwind
  reads from generated CSS variables via v4 `@theme`.

## Capabilities Owned

- Author the **DTCG JSON tokens.json** as the source of truth.
  Token categories per SOP §6.4.1 + E3 §6.1:
  - **Color** — primary / secondary / accent / background /
    surface / text (primary/secondary/tertiary) / error /
    warning / success / info, plus a complete shade scale per
    color (50–950).
  - **Typography** — font families (heading / body / mono),
    type scale (display / h1–h6 / body / caption), line
    heights, letter spacing, font weights.
  - **Spacing** — scale (e.g., 4 / 8 / 12 / 16 / 24 / 32 /
    48 / 64 / 96 / 128 px).
  - **Radius** — sharp / sm / md / lg / xl / full.
  - **Shadow / elevation** — raised / dialog / popover / etc.
  - **Motion** — consumes motion-language-author's tokens
    (durations + easings).
  - **Z-index** — base / raised / overlay / modal / toast /
    tooltip.
  - **Breakpoints** — mobile-first (sm / md / lg / xl / 2xl).
- Configure **Style Dictionary v4** with DTCG transforms via
  `@tokens-studio/sd-transforms` for the import side.
- Generate **outputs**:
  - `tokens.css` — CSS variables under `:root`.
  - `tokens.ts` — TypeScript exports (typed).
  - Tailwind v4 `@theme` block reading the CSS variables.
  - Optionally iOS / Android outputs if cross-platform.
- Set up the **CI gate** — a watch script in dev; a CI step
  that re-runs Style Dictionary and fails the build if
  outputs are stale relative to `tokens.json`.
- Refuse **CSS-in-JS at the token layer** (per E3 §6.1 anti-
  pattern: runtime cost). Tokens are static.
- Refuse **hand-coded `tailwind.config.ts` with hex values**.
- Cite **art direction** + **motion language** by stable name.
- Write to `design-tokens/{tokens.json, build-tokens.config.ts}`
  + generated outputs.

## Handoffs to Other Skills

- **From `art-direction-author`** — palette + type + spacing
  rules.
- **From `motion-language-author`** — motion tokens (durations
  + easings) flow in as one category.
- **To `component-states-matrix-author`** — state matrices
  reference tokens by stable name (`color-text-primary`,
  `motion-duration-fast`, etc.).
- **To `engineering-handoff-spec-author`** — the token system
  is part of the handoff package.
- **To Phase 4 build** — engineering consumes the generated
  outputs (CSS variables + Tailwind theme + TS types).
- **From the user-invocable `draft-design-system-tokens`** —
  peer skill producing the same artifact via a different
  procedure.

## Edge Cases

- **Project uses Tailwind v3** (not v4). Tailwind v3 doesn't
  read CSS variables natively in the config. Either upgrade
  to v4 or generate a Tailwind v3 config from the tokens
  with a Style Dictionary transform; document the friction
  (tokens-as-static-config is brittle to design changes).
- **Brand mandates a font with restrictive licensing.** The
  token references the font face; the licensing is captured
  in the art direction. This atom ships with the font name
  but doesn't ship the font file.
- **Multi-brand / multi-theme project.** Author a base token
  set + per-brand override sets. Style Dictionary handles
  themed builds. Refuse a single mega-token set with
  conflicting values.
- **Designers and engineers diverge** (designer adds a token
  in Figma but Tokens Studio export hasn't run; engineer
  hard-codes the value). Surface this as a finding in the
  Stage 6 family audit; the CI gate catches it on build.
- **Operator wants to skip tokens for a "small" project.**
  Refuse for projects with ≥3 templates (per SOP §6.4 — "the
  system pays for itself the moment a second template is
  built"). For single-page sites, acceptable to ship a
  minimal `:root` CSS-vars file without DTCG, but document
  why.

## References

No external `references/*.md` files yet — first real authoring
run will produce a template worth promoting. The canonical
authorities are `internal://docs/research/E3-technical-conventions.md`
§6.1 + the SOP §6.4.1. The W3C DTCG specification (stable Oct
2025) and Style Dictionary v4 are the named industry references.
The user-invocable `draft-design-system-tokens` is a peer skill
producing the same artifact via a different procedure.

## Self-Audit

Before declaring a token system complete, confirm:
- DTCG JSON is the source of truth (no hex values in
  Tailwind config).
- Style Dictionary v4 transforms produce CSS / TS / Tailwind
  outputs.
- All 8 token categories covered (color / type / spacing /
  radius / shadow / motion / z-index / breakpoints).
- Color scale runs 50–950 per color.
- CI gate exists (watch in dev + build-time staleness check).
- Motion tokens flow from motion-language-author.
- No CSS-in-JS at the token layer.
- Art direction + motion language cited by stable name.
