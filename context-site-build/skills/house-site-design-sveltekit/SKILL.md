---
name: house-site-design-sveltekit
description: >
  House conventions for the site-design family on the Combo D stack
  (SvelteKit + Vite + Tailwind + vanilla Three.js + GSAP + Histoire/
  Storybook). Overlays design-tokens-author, design-system-author,
  motion-language-author, engineering-handoff-spec-author, and
  component-states-matrix-author with stack-specific tooling (DTCG →
  Style Dictionary → CSS vars + Tailwind v4 + TS pipeline; vanilla
  Three.js wrapped in Svelte components; GSAP for marketing motion +
  Svelte's native crossfade/flip for UI; Histoire or Storybook for
  component dev). Do NOT use for: SRS / ADR / runbook / threat-model
  on SvelteKit (use house-site-build-sveltekit); launch / observability
  on SvelteKit hosts (use house-site-operate-sveltekit); cross-stack
  motion (use house-site-design-motion); Figma-tool integration (use
  house-site-design-figma); composing this overlay with a per-team
  overlay (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, stack-overlay]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 stack-
            overlay batch (SvelteKit × 3). Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-design-sveltekit

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay encoding Combo D's design-system + motion conventions
on top of the `site-design` family's mechanism atoms.

## Purpose

Encode how design tokens, components, and motion flow through a
SvelteKit + Svelte 5 codebase:

1. Design tokens follow the canonical DTCG → Style Dictionary v4 →
   CSS vars + Tailwind v4 + TS pipeline.
2. Components are Svelte 5 with runes (`$state`, `$derived`,
   `$effect`); components live in `src/lib/components/`.
3. Motion split: GSAP for marketing/scene direction; Svelte's
   built-in `<svelte:transition>` + `crossfade` + `flip` for UI
   motion.
4. 3D via **vanilla Three.js** wrapped in Svelte components (Igloo
   Inc precedent); Svelte-Cubed acceptable but less mature.
5. **Histoire** (Vite-native, framework-agnostic) OR Storybook (when
   org-wide multi-framework standardization) for component dev;
   visual regression via Lost Pixel / Playwright.

## Applies On Top Of

- `design-tokens-author` — emits DTCG JSON consumed by Style
  Dictionary v4.
- `design-system-author` — components ship as Svelte 5 SFCs with
  runes-based reactivity.
- `motion-language-author` — motion library selection per use case;
  Svelte's native motion primitives integrate with the design system.
- `engineering-handoff-spec-author` — handoff names the Histoire /
  Storybook URL + visual-regression baseline + token export hashes.
- `component-states-matrix-author` — 9-state matrix per Svelte
  component; CI gate.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Tokens pipeline

Same canonical pipeline as Combos A/B/C:

```
Figma Variables + Tokens Studio
        ↓ (export DTCG JSON)
tokens/*.json
        ↓ (Style Dictionary v4)
src/lib/styles/tokens.css       (CSS custom properties)
src/app.css                     (Tailwind v4 @theme block)
src/lib/tokens.ts               (TypeScript types)
```

Hand-coded `tailwind.config.ts` values forbidden; `tokens.json`
modified without regenerating outputs fails CI.

### Component conventions

- **Svelte 5 with runes** (`$state`, `$derived`, `$effect`,
  `$props`) for reactivity.
- **`src/lib/components/`** as the design-system component root;
  `+page.svelte` files compose them.
- **Composition over slots-per-flag**. Slots + named slots over
  many boolean props.
- **States naming**: `default | hover | focus-visible | active |
  disabled | loading | error | empty | skeleton`.
- **Histoire stories** (`*.story.svelte`) OR Storybook stories
  (`*.stories.svelte`); `controls` table is the API contract.

### Motion stack

| Use case | Library | Rationale |
|---|---|---|
| Marketing hero, scroll-driven scenes | **GSAP + ScrollTrigger** | Industry standard; MIT-licensed |
| App-shell UI transitions | **Svelte built-in** `transition:` directives + `crossfade` + `flip` | Native, zero deps; integrates with `{#if}`/`{#each}` |
| Designer-authored micro-animations | **Lottie / Rive** | Triggered via IntersectionObserver |
| Native scroll-driven (Chromium-only) | **Native CSS** `animation-timeline: scroll() / view()` | Progressive enhancement layer |

- **Lenis** integration via Svelte action (`use:lenis`); same scroll-
  source-of-truth pattern.
- **gsap.context** equivalent in Svelte: scope ScrollTrigger inside
  `onMount` + cleanup in `onDestroy`.
- **`crossfade`** for paired enter/leave transitions (e.g., card
  flying from grid → detail view).
- **`flip`** for List-Inside-View Permutation animations.

### 3D conventions (vanilla Three.js)

- **vanilla Three.js** is the default per E3 §5 Combo D / Igloo Inc.
- Three.js wrapped in a Svelte component with `onMount` / `onDestroy`
  for renderer lifecycle.
- **Asset pipeline**: glTF + Draco + KTX2 (same as other combos).
- **Post-processing**: Vanruesc's `postprocessing` library directly.
- **Svelte-Cubed** acceptable for simpler scenes where the Svelte-
  reactive bindings save scaffolding; document in ADR.

### Histoire / Storybook

- **Histoire** is the default for Svelte-only projects (Vite-native;
  ~1.5s cold start).
- **Storybook 8/9** when org-wide multi-framework standardization
  applies (Svelte preset matured 2024–2025).
- **MDX docs** for component prose.
- **Lost Pixel** or **Playwright `toHaveScreenshot()`** for visual
  regression.

## Override Behavior

This overlay applies when:

- The project's `srs-author` output cites Combo D.
- All five mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

If Svelte-Cubed proves insufficient for advanced 3D and the project
adopts an iframe-island bridge to R3F, document in ADR; this overlay
treats that as a hybrid case where parts ride this overlay and the
R3F island rides `house-site-design-nextjs` conventions in isolation.

The tokens-pipeline section is **non-overridable**: hand-coded
Tailwind theme values OR runtime CSS-in-JS for tokens are anti-
patterns.

For multi-stack projects, use `house-site-design-motion` for the
shared motion conventions and ride this overlay only on SvelteKit
surfaces.

Cross-cutting concerns defer to dedicated atoms per A62 anti-trigger
fallback. See `house-site-design-nextjs` for the canonical list.

## See Also

- `house-site-build-sveltekit` — SRS / ADR / schedule / runbook /
  threat-model conventions for Combo D.
- `house-site-operate-sveltekit` — launch + observability conventions
  for Combo D.
- `house-site-design-figma` — design-tool integration; tokens upstream.
- `house-site-design-motion` — cross-stack motion conventions.
- `house-site-design-a11y` — cross-stack a11y conventions.
- `docs/research/E3-technical-conventions.md` §2, §3, §6 — evidence.
