---
name: house-site-design-figma
description: >
  Design-tool overlay encoding the Figma + Tokens Studio + Auto Layout
  + Component Properties → DTCG JSON → Style Dictionary v4 → CSS vars
  + Tailwind v4 @theme + TypeScript types pipeline. Overlays
  design-tokens-author, design-system-author, engineering-handoff-spec-
  author, and component-states-matrix-author with Figma-specific
  conventions (Variables structure, Auto Layout discipline, Component
  Properties as the API contract, Tokens Studio export ritual,
  motion-spec via Theatre.js / Lottie / Rive in Storybook NOT Loom
  links). Stack-agnostic — applies regardless of frontend stack.
  Do NOT use for: motion-language conventions (use
  house-site-design-motion); WCAG-conformance (use
  house-site-design-a11y); Webflow Variables sync (covered in
  house-site-design-webflow); composing this overlay with a per-team
  overlay (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, design-tool]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 design-
            tool overlay batch. Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-design-figma

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Design-tool overlay codifying the canonical Figma → DTCG → Style
Dictionary → multi-output pipeline that has converged across mature
agency design systems in 2024–2025 (E3 §6.1, §6.6).

## Purpose

Encode how design tokens and component specs flow from Figma into
the codebase:

1. Figma is the source of truth for tokens, components, and motion
   specs.
2. Tokens flow Figma Variables → Tokens Studio (plugin) → DTCG JSON
   → Style Dictionary v4 → CSS variables + Tailwind v4 `@theme` +
   TypeScript types.
3. Component specs flow Figma Components → Component Properties
   (the API contract) → engineering handoff (which Storybook story
   matches which Figma component).
4. Component states use Figma Variants for the 9 named states.
5. Motion specs use Theatre.js / Lottie / Rive embedded in Storybook
   — NOT Loom links (which decay).
6. Hand-coded `tailwind.config.ts` with hex values is an anti-pattern
   the overlay explicitly rejects.

## Applies On Top Of

- `design-tokens-author` — the tokens output is DTCG JSON consumed
  by Style Dictionary v4 with `@tokens-studio/sd-transforms`.
- `design-system-author` — Figma Components + Component Properties
  are the upstream specs; Storybook is the rendered system.
- `engineering-handoff-spec-author` — handoff names the Figma file
  URL + Tokens Studio sync version + Storybook URL + token export
  hash.
- `component-states-matrix-author` — Figma Variants encode the 9
  states; the matrix is generated from variants and rendered in
  Storybook.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Tokens pipeline (the canonical chain)

```
┌─ Figma Variables (color / size / spacing / typography)
│   + Component Properties (the API contract)
│   + Auto Layout (the responsive contract)
│   ↓
├─ Tokens Studio plugin
│   (export DTCG JSON)
│   ↓
├─ tokens/*.json  (in repo)
│   ↓
├─ Style Dictionary v4 + @tokens-studio/sd-transforms
│   ↓
├─ src/styles/tokens.css     (CSS custom properties)
├─ src/styles/tailwind.css   (Tailwind v4 @theme block)
└─ src/lib/tokens.ts         (TypeScript types + values)
```

- **Source of truth is Figma**. Hand-coded `tailwind.config.ts`
  with hex values is **forbidden**.
- **CI gate**: `tokens.json` modified without regenerating outputs
  fails the build. The build script is `npm run tokens` (or `pnpm
  tokens`); CI runs `npm run tokens:check`.
- **Tailwind v4 `@theme`** reads CSS variables; do not hard-code
  Tailwind theme values.
- **CSS-in-JS for tokens** is forbidden — runtime cost (E3 §6.1).

### Figma Variables structure

- **Per-mode collections**: light / dark / high-contrast as Variable
  Mode collections (when applicable).
- **Per-brand collections**: when a project has multiple brands,
  each is a Mode within the same collection.
- **Naming convention**: `<scope>/<role>/<step>` slash-separated
  (e.g., `color/primary/500`, `spacing/inline/3`).
- **Aliasing**: tokens reference other tokens within Figma; the
  alias chain is preserved through the export.

### Component Properties as the API contract

- **Variants** for state changes (default / hover / focus / etc.) +
  intent (primary / secondary / ghost) + size (sm / md / lg).
- **Boolean properties** for binary feature flags (`hasIcon`,
  `isLoading`).
- **Instance swap** for slot-shaped composition (icon slots,
  content slots).
- **Text properties** for content overrides.

The 1:1 contract: every Component Property maps to a TypeScript
prop in the engineering counterpart; Storybook controls render the
same set.

### Component states matrix (the 9 states)

| State | Figma encoding |
|---|---|
| default | Default variant |
| hover | Variant: state=hover (hover preview prototype interaction) |
| focus-visible | Variant: state=focus |
| active | Variant: state=active |
| disabled | Variant: state=disabled |
| loading | Variant: state=loading (typically with Lottie/Rive embed) |
| error | Variant: state=error |
| empty | Variant: state=empty (typically a separate empty-state component) |
| skeleton | Variant: state=skeleton |

The CI gate refuses "ready" mark on a component missing any of
the 9 states.

### Motion specs (citing E3 §6.3)

| Spec form | Use case | Status |
|---|---|---|
| **Theatre.js studio captures** | Motion-designer-led timelines | ✅ recommended |
| **Lottie / Rive files** + Storybook-embedded preview | Designer-authored micro-animations | ✅ recommended |
| **Motion principles doc** in `docs/motion.md` | Project-wide motion language | ✅ required |
| **Motion tokens** in design system | Reusable durations / easings | ✅ required |
| **Figma Smart Animate / Motion plugin screencaps** | Quick handoff | ⚠️ fragile; common in practice |
| **Loom links** as motion spec | — | ❌ they decay; do not use |

### Engineering handoff scope

The handoff document (from `engineering-handoff-spec-author`)
includes:

- **Figma file URL** with anchor links to specific frames.
- **Tokens Studio sync version** (the JSON snapshot hash).
- **Storybook URL** + the canonical baseline ID.
- **Component-property → TypeScript-prop mapping table** (the API
  contract).
- **Motion spec links** (Theatre.js project ID, Lottie file URL,
  Rive file URL — not Loom links).

## Override Behavior

This overlay applies when:

- The project uses Figma as the design tool.
- All four mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

The "Loom link as motion spec" anti-pattern is **non-overridable**.
The "hand-coded `tailwind.config.ts` hex values" anti-pattern is
**non-overridable**. The "CSS-in-JS for tokens" anti-pattern is
**non-overridable**. Projects that insist on these patterns should
not be using this overlay.

For projects that use a non-Figma design tool (Penpot, Sketch,
Adobe XD), this overlay does not apply; the tokens-pipeline
discipline still applies but the upstream source-of-truth section
needs adaptation per the chosen tool's export format.

For Webflow projects: Webflow Variables are the platform-native
source-of-truth; Tokens Studio sync is limited per
`house-site-design-webflow`. This overlay's pipeline becomes
advisory in that context.

## See Also

- `house-site-design-{nextjs,nuxt,astro,sveltekit}` — per-stack
  design overlays that consume this overlay's tokens pipeline
  output.
- `house-site-design-webflow` — Webflow's adaptation (limited
  Tokens Studio sync).
- `house-site-design-motion` — cross-stack motion conventions; this
  overlay's motion-spec section pairs with that overlay's library
  selection.
- `docs/research/E3-technical-conventions.md` §6.1, §6.3, §6.6 —
  evidence base.
