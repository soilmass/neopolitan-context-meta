---
name: house-site-design-nextjs
description: >
  House conventions for the site-design family on the Combo A stack
  (Next.js + React + R3F + GSAP + Storybook + Chromatic). Overlays
  design-tokens-author, design-system-author, motion-language-author,
  engineering-handoff-spec-author, and component-states-matrix-author
  with stack-specific tooling (DTCG → Style Dictionary v4 → CSS vars +
  Tailwind v4 @theme + TS types pipeline; React Three Fiber + drei +
  Framer Motion; ScrollTrigger + Lenis via @14islands/r3f-scroll-rig).
  Do NOT use for: SRS / ADR / runbook / threat-model conventions on
  Next.js (use house-site-build-nextjs); launch / observability
  conventions on Vercel (use house-site-operate-nextjs); cross-stack
  motion conventions when the project is multi-stack (use
  house-site-design-motion); design-tool integration with Figma
  specifically (use house-site-design-figma); composing this overlay
  with a per-team overlay (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, stack-overlay]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 stack-
            overlay batch (Next.js × 3). Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-design-nextjs

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay encoding Combo A's design-system + motion conventions
on top of the `site-design` family's mechanism atoms.

## Purpose

Encode how design-system tokens, components, and motion flow through
a Next.js + React codebase:

1. Design tokens follow the canonical DTCG JSON → Style Dictionary v4
   → CSS variables + Tailwind v4 `@theme` + TypeScript types pipeline.
2. Components are authored with React Server Components by default,
   with `"use client"` only where interactivity demands.
3. Motion is split: GSAP + ScrollTrigger for marketing/scene direction,
   Motion (Framer Motion) for app UI, native CSS scroll-driven
   animations as a progressive-enhancement layer.
4. Smooth scroll uses Lenis via `@14islands/r3f-scroll-rig` when
   WebGL-DOM sync is needed.
5. Storybook 8/9 + Chromatic is the design-review surface and visual-
   regression gate; it is part of CI, not ancillary.

## Applies On Top Of

- `design-tokens-author` — tokens emit DTCG JSON consumed by Style
  Dictionary v4; outputs include `tokens.css` (CSS vars), Tailwind v4
  `@theme` block, and `tokens.ts` (TS types).
- `design-system-author` — components ship as React Server Components
  by default; `"use client"` boundaries documented in the system.
- `motion-language-author` — motion library selection rules per use
  case; motion tokens follow `{prefix}-motion-{property}-{modifier}`
  naming.
- `engineering-handoff-spec-author` — handoff deliverable names the
  Storybook URL + Chromatic baseline + token export hashes.
- `component-states-matrix-author` — 9-state matrix is auto-generated
  from Storybook stories; CI gate refuses "ready" mark on a component
  missing any state.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Tokens pipeline (citing E3 §6.1, §6.6)

```
Figma Variables + Tokens Studio
        ↓ (export DTCG JSON)
tokens/*.json
        ↓ (Style Dictionary v4 + @tokens-studio/sd-transforms)
src/styles/tokens.css      (CSS custom properties)
src/styles/tailwind.css    (Tailwind v4 @theme block)
src/lib/tokens.ts          (TypeScript types + values)
```

- **Source of truth is Figma**; hand-coded tokens in
  `tailwind.config.ts` are forbidden.
- **CI gate**: `tokens.json` modified without regenerating outputs
  fails the build. The build script is `npm run tokens` (or
  `pnpm tokens`); CI runs `npm run tokens:check` which fails if
  outputs are stale.
- **Tailwind v4 `@theme`** reads CSS variables; do not hard-code
  Tailwind theme values. (CSS-in-JS for tokens is forbidden — runtime
  cost.)

### Component conventions

- **RSC by default.** A new component is a Server Component unless
  it needs interactivity (state, events, browser APIs).
- **`"use client"` boundaries are top-of-tree.** Marker goes on the
  smallest interactive subtree; do not mark every leaf.
- **Composition over props explosion.** Prefer slot-shaped APIs
  (`<Card.Header />`, `<Card.Body />`) over many boolean props.
- **States naming.** `default | hover | focus-visible | active |
  disabled | loading | error | empty | skeleton` — the 9-state
  matrix; component is not "ready" without all 9 stubbed.
- **Storybook autodocs** generated from component TSDoc; `args` table
  is the API contract.

### Motion stack (citing E3 §2.1, §2.3)

| Use case | Library | Rationale |
|---|---|---|
| Marketing hero, scroll-driven scenes, complex sequenced timelines | **GSAP + ScrollTrigger / SplitText / Flip** | Industry standard since 2024; MIT-licensed including all plugins |
| App-shell UI, layout transitions, gestures, exit animations | **Motion (Framer Motion)** | React-native; React 19 compatible; layout animations cheap |
| Tiny/CMS sites, design-system primitives | **Motion One** (vanilla WAAPI) | 3.8 KB animate fn; design-system layer |
| Simple parallax / reveal where Chromium-only acceptable | **Native CSS** `animation-timeline: scroll() / view()` | Progressive enhancement layer |
| Designer-authored micro-animations, illustrations | **Lottie / Rive** | Triggered via IntersectionObserver |

- **One global ScrollTrigger + Lenis bootstrap** at the app root;
  ScrollTrigger `.scrollerProxy()` sets Lenis as scroll source-of-truth.
- **Scenes scoped per chapter** via `gsap.context(() => { ... }, ref)`
  or the `useGSAP` hook so unmounting cleans up triggers.
- **`scrub: true`** for tight scroll-coupled motion; otherwise
  `toggleActions` with named labels.
- **For R3F**: use drei's `ScrollControls` + `useScroll().offset` paired
  with `useGSAP` for HTML overlays; or feed ScrollTrigger's `progress`
  into `useFrame`.
- **Theatre.js** when motion designers need timeline-grade authoring.

### 3D conventions (R3F + drei)

- **R3F** is the default for 3D in this stack; vanilla Three.js only
  when raw WebGL/WebGPU pipeline control is needed (memory pooling,
  custom render targets).
- **drei helpers** for loaders (Draco, KTX2), controls (OrbitControls),
  environment lighting, instancing, shaders. drei collapses 20–30
  lines of vanilla setup into 1–2.
- **Asset pipeline**: glTF + Draco geometry + KTX2 textures via
  `gltf-transform optimize --compress draco --texture-compress ktx2`.
- **Post-processing**: `@react-three/postprocessing` (Vanruesc's
  `postprocessing` library under the hood) over Three's stock
  `EffectComposer`.

### Storybook + Chromatic

- **Storybook 8/9** in `.storybook/`; React 19 + Next.js framework
  preset.
- **Chromatic** for visual regression; `chromatic` step in CI on every
  PR; baselines stored on `main`.
- **MDX docs** for component prose; `args` for the runtime API.
- **Ladle** is acceptable for solo-dev portfolios where Storybook's
  startup time is friction; otherwise Storybook is canonical.

## Override Behavior

This overlay applies when:

- The project's `srs-author` output cites Combo A.
- All five mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.
Per `ARCHITECTURE.md` §"Mechanism vs Policy", silent substitution is
forbidden.

If the project's stack diverges from Combo A, the operator either
switches to a different stack overlay (`house-site-design-{nuxt,
astro, sveltekit, webflow}`) or documents the divergence in an ADR.

The tokens-pipeline section is **non-overridable**: hand-coded
Tailwind theme values OR runtime CSS-in-JS for tokens are anti-
patterns the overlay explicitly rejects. If a project insists on
either, it should not be using this overlay.

For multi-stack projects (rare — typically a marketing site + an app
shell on different stacks), use `house-site-design-motion` for the
shared motion conventions and ride this overlay only on the Next.js
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

- `house-site-build-nextjs` — SRS / ADR / schedule / runbook /
  threat-model conventions for the same stack.
- `house-site-operate-nextjs` — launch + observability conventions
  for the same stack.
- `house-site-design-figma` — design-tool integration; tokens pipeline
  upstream.
- `house-site-design-motion` — cross-stack motion conventions (this
  overlay covers the React-specific layer; `-motion` covers the
  stack-agnostic layer).
- `house-site-design-a11y` — cross-stack a11y conventions for motion-
  heavy sites.
- `docs/research/E3-technical-conventions.md` §2, §3, §6 — evidence.
