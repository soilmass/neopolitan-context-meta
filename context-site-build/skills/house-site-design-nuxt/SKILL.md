---
name: house-site-design-nuxt
description: >
  House conventions for the site-design family on the Combo B stack
  (Nuxt 3 + Vue 3 + Tailwind + TresJS + GSAP + Histoire). Overlays
  design-tokens-author, design-system-author, motion-language-author,
  engineering-handoff-spec-author, and component-states-matrix-author
  with stack-specific tooling (DTCG → Style Dictionary v4 → CSS vars +
  Tailwind v4 @theme + TS types pipeline; TresJS for 3D; GSAP for
  marketing motion + Vue native transitions for UI; Histoire for
  component dev). Do NOT use for: SRS / ADR / runbook / threat-model
  on Nuxt (use house-site-build-nuxt); launch / observability on Nuxt
  hosts (use house-site-operate-nuxt or host-specific overlay); cross-
  stack motion conventions (use house-site-design-motion); Figma-tool
  integration (use house-site-design-figma); composing this overlay
  with a per-team overlay (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, stack-overlay]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 stack-
            overlay batch (Nuxt × 3). Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-design-nuxt

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay encoding Combo B's design-system + motion conventions
on top of the `site-design` family's mechanism atoms.

## Purpose

Encode how design tokens, components, and motion flow through a
Nuxt 3 + Vue codebase:

1. Design tokens follow the canonical DTCG JSON → Style Dictionary v4
   → CSS variables + Tailwind v4 `@theme` + TypeScript types pipeline
   (same as Combo A — the pipeline is stack-agnostic).
2. Components are Vue 3 SFCs with `<script setup>`; auto-imported via
   Nuxt's component discovery; explicit imports only when the linter
   flags ambiguity.
3. Motion split: GSAP + ScrollTrigger for marketing/scene direction,
   Vue's native `<Transition>` / `<TransitionGroup>` for UI.
4. 3D via **TresJS** (Vue-native wrapper around Three.js); raw
   Three.js only when TresJS doesn't cover the need.
5. **Histoire** (Vue-native Storybook alternative) is the design-review
   surface; visual regression via Lost Pixel or Playwright
   `toHaveScreenshot()`.

## Applies On Top Of

- `design-tokens-author` — tokens emit DTCG JSON consumed by Style
  Dictionary v4; outputs include `tokens.css`, Tailwind v4 `@theme`,
  `tokens.ts`.
- `design-system-author` — components ship as Vue 3 SFCs;
  auto-imported via `components/` directory.
- `motion-language-author` — motion library selection rules per use
  case; motion tokens follow `{prefix}-motion-{property}-{modifier}`.
- `engineering-handoff-spec-author` — handoff names the Histoire URL
  + visual-regression baseline + token export hashes.
- `component-states-matrix-author` — 9-state matrix auto-generated
  from Histoire stories; CI gate refuses "ready" without all 9.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Tokens pipeline

Same canonical pipeline as Combo A:

```
Figma Variables + Tokens Studio
        ↓ (export DTCG JSON)
tokens/*.json
        ↓ (Style Dictionary v4 + @tokens-studio/sd-transforms)
assets/tokens.css       (CSS custom properties)
assets/tailwind.css     (Tailwind v4 @theme block)
shared/tokens.ts        (TypeScript types + values)
```

- **Source of truth is Figma**; hand-coded tokens in
  `tailwind.config.ts` are forbidden.
- **CI gate**: `tokens.json` modified without regenerating outputs
  fails the build.
- **Tailwind v4 `@theme`** reads CSS variables; do not hard-code
  Tailwind theme values.

### Component conventions

- **Vue 3 SFCs** with `<script setup lang="ts">`; Composition API
  default.
- **Auto-imported** via Nuxt's `components/` directory; explicit
  import only when ambiguity surfaces.
- **Composition over props explosion.** Prefer slot-shaped APIs
  (`<Card><template #header>`) over many boolean props.
- **States naming**: `default | hover | focus-visible | active |
  disabled | loading | error | empty | skeleton` — the 9-state matrix.
- **Histoire stories** use the `*.story.vue` convention; `controls`
  table is the API contract.

### Motion stack

| Use case | Library | Rationale |
|---|---|---|
| Marketing hero, scroll-driven scenes, complex sequenced timelines | **GSAP + ScrollTrigger / SplitText / Flip** | Industry standard; MIT-licensed |
| App-shell UI, layout transitions | **Vue `<Transition>` / `<TransitionGroup>`** | Native, zero deps; integrates with `v-if` / `v-show` |
| Designer-authored micro-animations | **Lottie / Rive** | Triggered via IntersectionObserver |
| Native scroll-driven (Chromium-only) | **Native CSS** `animation-timeline: scroll() / view()` | Progressive enhancement |
| Complex Vue UI motion beyond `<Transition>` | **@vueuse/motion** | Vue-native motion library; light alternative to GSAP for non-marketing UI |

- **Lenis** integration via `vue-lenis` or manual init in a Nuxt
  plugin; same scroll-source-of-truth pattern as Combo A.
- **gsap.context** equivalent in Vue: scope ScrollTrigger inside
  `onMounted` + cleanup in `onUnmounted`.

### 3D conventions (TresJS)

- **TresJS** is the default for 3D in Nuxt; it wraps Three.js with
  Vue 3 reactivity.
- **`@tresjs/cientos`** is the drei-equivalent helpers package
  (loaders, controls, environment, instancing).
- **`@tresjs/post-processing`** for post-processing effects.
- **Asset pipeline**: glTF + Draco geometry + KTX2 textures; same as
  Combo A.
- **Raw Three.js** is acceptable when TresJS lacks the API; wrap in a
  thin Vue component to keep reactivity.

### Histoire + visual regression

- **Histoire** in `histoire.config.ts`; Vue 3 + Vite preset.
- **Lost Pixel** or **Playwright `toHaveScreenshot()`** for visual
  regression (Histoire lacks Chromatic equivalent; Lost Pixel is the
  rising open-source pick).
- **MDX docs** via Histoire's docs blocks; `controls` for runtime API.
- **Storybook** is acceptable when an org standardizes on it across
  Vue + React; Histoire is the Vue-native default.

## Override Behavior

This overlay applies when:

- The project's `srs-author` output cites Combo B.
- All five mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.
Per `ARCHITECTURE.md` §"Mechanism vs Policy", silent substitution is
forbidden.

If the project's stack diverges from Combo B, the operator either
switches stack overlays or documents the divergence in an ADR.

The tokens-pipeline section is **non-overridable**: hand-coded
Tailwind theme values OR runtime CSS-in-JS for tokens are anti-
patterns the overlay explicitly rejects.

For multi-stack projects, use `house-site-design-motion` for the
shared motion conventions and ride this overlay only on the Nuxt
surfaces.

Cross-cutting concerns defer to dedicated atoms per A62 anti-trigger
fallback:

- WCAG 2.2 motion-criteria conformance — use
  `motion-conformance-author`; the user-invocable
  `draft-motion-conformance` covers it now.
- Performance budgets enforced in CI — use
  `performance-budget-author`; the user-invocable
  `draft-perf-budget` covers it now.

## See Also

- `house-site-build-nuxt` — SRS / ADR / schedule / runbook /
  threat-model conventions for Combo B.
- `house-site-operate-nuxt` — launch + observability conventions for
  Combo B.
- `house-site-design-figma` — design-tool integration; tokens pipeline
  upstream.
- `house-site-design-motion` — cross-stack motion conventions.
- `house-site-design-a11y` — cross-stack a11y conventions for motion-
  heavy sites.
- `docs/research/E3-technical-conventions.md` §2, §3, §6 — evidence.
