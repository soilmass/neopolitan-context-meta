---
name: house-site-design-astro
description: >
  House conventions for the site-design family on the Combo C stack
  (Astro + Vite + Tailwind + framework islands + vanilla Three.js or
  R3F island + GSAP + Lenis on hero islands only). Overlays
  design-tokens-author, design-system-author, motion-language-author,
  engineering-handoff-spec-author, and component-states-matrix-author
  with stack-specific tooling (DTCG → Style Dictionary → CSS vars +
  Tailwind v4 + TS pipeline; vanilla Three.js + Alien.js or React
  island R3F; GSAP + Lenis hero-island-only; Storybook or Ladle).
  Do NOT use for: SRS / ADR / runbook / threat-model on Astro (use
  house-site-build-astro); launch / observability on Astro hosts (use
  house-site-operate-astro); cross-stack motion (use
  house-site-design-motion); Figma-tool integration (use
  house-site-design-figma); composing this overlay with a per-team
  overlay (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, stack-overlay]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 stack-
            overlay batch (Astro × 3). Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-design-astro

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay encoding Combo C's design-system + motion conventions
on top of the `site-design` family's mechanism atoms.

## Purpose

Encode how design tokens, components, and motion flow through an
Astro + island-architecture codebase:

1. Design tokens follow the canonical DTCG → Style Dictionary v4 →
   CSS vars + Tailwind v4 + TS pipeline (stack-agnostic).
2. Components are Astro `.astro` files for static parts; framework-
   native files (`.tsx`/`.vue`/`.svelte`) inside `src/components/<fw>/`
   for island parts.
3. Motion split: vanilla Three.js + Alien.js for stack-native 3D, OR
   R3F island when React justified; GSAP for marketing scenes; Lenis
   only on hero islands (NOT long-form content per E3 §2.2).
4. Storybook (with the appropriate framework preset) OR Ladle (React-
   only) for component dev; visual regression via Lost Pixel /
   Playwright.

## Applies On Top Of

- `design-tokens-author` — emits DTCG JSON consumed by Style
  Dictionary v4.
- `design-system-author` — components are split across `.astro`
  (static) and framework-native (island).
- `motion-language-author` — motion library selection per island
  pattern; hero-island-only Lenis discipline.
- `engineering-handoff-spec-author` — handoff names the Storybook /
  Ladle URL + visual-regression baseline.
- `component-states-matrix-author` — 9-state matrix per framework-
  native component; Astro components are typically stateless and
  exempt from the matrix.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Tokens pipeline

Same canonical pipeline as Combos A/B:

```
Figma Variables + Tokens Studio
        ↓ (export DTCG JSON)
tokens/*.json
        ↓ (Style Dictionary v4)
src/styles/tokens.css       (CSS custom properties)
src/styles/tailwind.css     (Tailwind v4 @theme block)
src/lib/tokens.ts           (TypeScript types)
```

Hand-coded `tailwind.config.ts` values forbidden; `tokens.json`
modified without regenerating outputs fails CI.

### Component conventions

- **`.astro` files** for static parts (no JS shipped unless directive
  applied).
- **Framework-native files** (`.tsx`/`.vue`/`.svelte`) in
  `src/components/<framework>/` for islands.
- **Single-framework default**; mixing frameworks requires ADR
  justification.
- **Hydration directives** chosen per island per the build overlay's
  policy doc.
- **States naming** for framework-native components: `default | hover |
  focus-visible | active | disabled | loading | error | empty |
  skeleton`.

### Motion stack

- **GSAP + ScrollTrigger** for marketing/scene direction (loaded only
  on pages that need it via island OR `is:inline` script).
- **Native CSS** for cheap reveal/parallax (Chromium-only fallback
  acceptable for progressive enhancement).
- **Lenis** only on hero islands; long-form content uses native
  scroll. Per E3 §2.2: Lenis hijacks wheel/touch and breaks scanning
  on docs / blogs.
- **Howler** for audio integration when needed (Combo C is the only
  combo where audio is reliably called out — Rogier de Boevé Portfolio
  2024 baseline).
- **Lottie / Rive** for designer-authored micro-animations.

### 3D conventions

| When | Library |
|---|---|
| Hero is the page chrome; rest is HTML/CSS | **vanilla Three.js + Alien.js** |
| Hero is React-rich (lots of UI overlaid on canvas) | **React island with R3F + drei** |
| Hero is Vue-rich | **Svelte island with Svelte-Cubed** OR vanilla Three.js wrapped in a Vue island |
| Mid-page interactive 3D | Vanilla preferred (smaller payload) |

- **Asset pipeline**: glTF + Draco + KTX2 (same as Combos A/B).
- **Post-processing**: Vanruesc's `postprocessing` library directly
  (no React wrapper) when on vanilla Three.js.

### Storybook / Ladle

- **Storybook 8/9** when component matrix spans multiple frameworks
  (Astro projects mixing React + Vue + Svelte islands).
- **Ladle** for solo-dev / single-framework (React-only) projects
  where startup time matters (1.2s cold vs Storybook's 8s).
- **Histoire** when single-framework Vue.
- **Lost Pixel** or **Playwright `toHaveScreenshot()`** for visual
  regression.

## Override Behavior

This overlay applies when:

- The project's `srs-author` output cites Combo C.
- All five mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

If the project moves to single-framework (e.g., all-React via Astro's
React adapter), the multi-framework component conventions become
advisory.

The tokens-pipeline section is **non-overridable**: hand-coded
Tailwind theme values OR runtime CSS-in-JS for tokens are anti-
patterns.

For multi-stack projects, use `house-site-design-motion` for shared
motion conventions and ride this overlay only on Astro surfaces.

Cross-cutting concerns defer to dedicated atoms per A62 anti-trigger
fallback. See `house-site-design-nextjs` for the canonical fallback
list.

## See Also

- `house-site-build-astro` — SRS / ADR / schedule / runbook / threat-
  model conventions for Combo C.
- `house-site-operate-astro` — launch + observability conventions for
  Combo C.
- `house-site-design-figma` — design-tool integration; tokens upstream.
- `house-site-design-motion` — cross-stack motion conventions.
- `house-site-design-a11y` — cross-stack a11y conventions.
- `docs/research/E3-technical-conventions.md` §2, §3, §6 — evidence.
