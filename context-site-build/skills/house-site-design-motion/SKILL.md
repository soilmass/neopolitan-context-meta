---
name: house-site-design-motion
description: >
  Cross-stack motion conventions overlaid on motion-language-author,
  design-tokens-author, and design-system-author. Encodes the canonical
  R3F + drei + GSAP + Lenis vs vanilla Three.js patterns; motion-token
  schema (motion-duration-* / motion-ease-*); GSAP timelines as motion
  spec for engineer-led teams; Theatre.js for motion-designer-led
  teams; Lottie/Rive for designer-authored micro-animations;
  ScrollTrigger gsap.context discipline for scene scoping. Stack-
  agnostic — applies on top of any of the 5 frontend stack overlays
  (Next.js / Nuxt / Astro / SvelteKit / Webflow). Do NOT use for: WCAG
  motion-criteria conformance (use house-site-design-a11y); stack-
  specific motion library selection rules (use the per-stack design
  overlay e.g. house-site-design-nextjs); composing this overlay with
  a per-team overlay (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, cross-stack]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 cross-
            stack overlay batch. Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-design-motion

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Cross-stack overlay encoding canonical motion conventions that apply
across all 5 frontend stack combos. Use this overlay when a project's
motion sophistication exceeds what the per-stack overlay covers, or
when a multi-stack project needs shared motion conventions.

## Purpose

Encode the conventions that produce Awwwards-tier motion regardless
of stack:

1. Motion tokens follow the canonical
   `{prefix}-motion-{property}-{modifier}` naming; tokens flow through
   the design system (CSS variables + Tailwind v4 `@theme` + TS
   types).
2. The library choice per use case is named explicitly with the
   rationale (E3 §2.1 "Current consensus 2024-2025").
3. Scene scoping uses GSAP's `gsap.context` (or framework equivalents
   — Vue's `onMounted/onUnmounted`, Svelte's `onMount/onDestroy`,
   React's `useGSAP`) so unmounting cleans up triggers; without this
   discipline, ScrollTrigger leaks accumulate.
4. Motion specs go via Theatre.js (motion-designer-led) or GSAP
   timelines as the spec (engineer-led); Loom links and Figma Smart
   Animate are anti-patterns because they decay.
5. Lottie / Rive carry designer-authored micro-animations.

## Applies On Top Of

- `motion-language-author` — adds the motion-token schema + the
  cross-stack library-selection table; encodes scene-scoping
  discipline.
- `design-tokens-author` — adds the motion-token names (motion-
  duration-* / motion-ease-* / motion-distance-*) to the DTCG
  schema.
- `design-system-author` — adds the motion-spec section to the
  design system; documents which motions are "expressive" vs
  "productive" (the IBM Carbon taxonomy) or
  "informative/focused/expressive × hierarchy/feedback/status/
  character" (Material).

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Motion-token schema (citing E3 §6.3)

Names follow `{prefix}-motion-{property}-{modifier}`:

```
motion-duration-fast       → 100ms
motion-duration-medium     → 200ms
motion-duration-slow       → 400ms
motion-duration-very-slow  → 800ms

motion-ease-out            → cubic-bezier(0.16, 1, 0.3, 1)
motion-ease-in-out         → cubic-bezier(0.65, 0, 0.35, 1)
motion-ease-bounce         → cubic-bezier(0.68, -0.55, 0.265, 1.55)
motion-ease-emphasized     → cubic-bezier(0.05, 0.7, 0.1, 1)

motion-distance-1          → 8px   (token-step)
motion-distance-2          → 16px
motion-distance-3          → 24px
```

- **Source of truth** is Figma Variables → Tokens Studio → DTCG
  JSON → Style Dictionary; same pipeline as color / size tokens.
- **Two named motion taxonomies** in active use; project picks one
  in an ADR:
  - **IBM Carbon model**: motion as `expressive` vs `productive`.
  - **Material model**: `informative / focused / expressive` ×
    `hierarchy / feedback / status / character`.

### Library selection per use case

| Use case | Library | Rationale |
|---|---|---|
| Marketing hero, scroll-driven scenes, complex sequenced timelines | **GSAP + ScrollTrigger / SplitText / Flip** | Industry standard since 2024; MIT-licensed |
| App-shell UI (React) | **Motion (Framer Motion)** | React-native; layout animations cheap |
| App-shell UI (Vue) | Vue native `<Transition>` + `@vueuse/motion` | Native; integrates with `v-if` / `v-show` |
| App-shell UI (Svelte) | Svelte native `transition:` + `crossfade` + `flip` | Native; integrates with `{#if}` / `{#each}` |
| App-shell UI (vanilla / cross-framework) | **Motion One** (vanilla WAAPI) | 3.8 KB animate fn |
| Tiny / CMS sites | **Motion One** + native CSS | Minimal payload |
| Simple parallax / reveal (Chromium-only acceptable) | Native CSS `animation-timeline: scroll() / view()` | Progressive enhancement |
| Designer-authored micro-animations | **Lottie / Rive** | Triggered via IntersectionObserver |
| Motion-designer-led timeline authoring | **Theatre.js** | Visual scrubber; replaces fragile Loom links |

### Scene scoping discipline

The dominant agency pattern (visible across Codrops case studies,
GSAP forums, 14islands open source):

- **One global ScrollTrigger + Lenis (or ScrollSmoother) bootstrap**
  at the app root. ScrollTrigger `.scrollerProxy()` makes Lenis's
  virtualized scroll position the source of truth.
- **Scenes scoped per "chapter"** — each scroll section is wrapped:
  - React: `useGSAP(() => { ... }, { scope: ref })`
  - Vue: `gsap.context(() => { ... }, scope)` inside
    `onMounted`; `cleanup` in `onUnmounted`
  - Svelte: scope inside `onMount`; manual cleanup in `onDestroy`
  - Vanilla: `gsap.context(() => { ... }, container)` with
    `ctx.revert()` on tear-down
- **`scrub: true`** for tight scroll-coupled motion; otherwise
  `toggleActions` with named labels.
- **`pin: true`** for long-form pinned scenes — the workhorse of
  scrolly-telling hero sequences.
- **For R3F**: drei's `ScrollControls` + `useScroll().offset` paired
  with `useGSAP` for HTML overlays; OR feed ScrollTrigger's
  `progress` value into `useFrame`.

### Spec authoring (and anti-patterns)

| Pattern | Status |
|---|---|
| **Motion principles doc** (durations, easings, choreography rules) in `docs/motion.md` | ✅ recommended |
| **Motion tokens in design system** (motion-duration-* / motion-ease-*) | ✅ required |
| **Lottie / Rive files** + Storybook-embedded previews | ✅ for designer-authored |
| **Theatre.js studio captures** | ✅ for motion-designer-led timelines |
| **GSAP Timelines as spec** | ✅ for engineer-led teams |
| **Figma Smart Animate / Motion plugin screencaps** | ⚠️ fragile; common in practice |
| **Loom links as motion spec** | ❌ they decay; do not use |

## Override Behavior

This overlay applies when:

- The project's `srs-author` output cites motion as load-bearing
  (cinematic site, scrolly-telling, animated marketing hero).
- All three mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

This overlay is **stack-agnostic** by design — it overlays
mechanism atoms regardless of which per-stack design overlay is
also active. When both this overlay AND a per-stack design overlay
apply, the per-stack overlay's library-selection rules govern (it
knows the stack's framework-native motion primitives), and this
overlay's discipline (scene scoping, motion-token schema,
spec authoring) governs the cross-stack patterns.

The Loom-link anti-pattern is **non-overridable**: if a project
insists on Loom links as motion spec, the spec will decay and the
implementation will drift. Document the violation explicitly.

WCAG 2.2 motion-criteria conformance is OUT OF SCOPE for this
overlay; that's `house-site-design-a11y` paired with
`motion-conformance-author` (PR #7 / v0.6.0). Per A62 anti-trigger
fallback: use `motion-conformance-author` once built; the user-
invocable `draft-motion-conformance` covers it now.

## See Also

- `house-site-design-a11y` — WCAG 2.2 motion-criteria conformance.
- `house-site-design-{nextjs,nuxt,astro,sveltekit,webflow}` — per-
  stack design overlays; this overlay rides on top of any of them
  for cross-stack motion conventions.
- `motion-language-author` (mechanism atom) — what this overlay
  modifies.
- `docs/research/E3-technical-conventions.md` §2 (motion library
  stack), §6.3 (motion specs) — evidence base.
