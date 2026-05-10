---
name: house-site-design-webflow
description: >
  House conventions for the site-design family on the Webflow stack
  (Webflow Designer + Variables + Components + Style Guide page).
  Overlays design-tokens-author, design-system-author, motion-language-
  author, engineering-handoff-spec-author, and component-states-matrix-
  author with Webflow-specific tooling (Webflow Variables as token
  source-of-truth; Tokens Studio sync where API permits; GSAP via
  custom-code embed for cinematic motion; Webflow Components as the
  design system; Style Guide page rendered live). Do NOT use for: SRS
  / ADR / runbook / threat-model on Webflow (use house-site-build-
  webflow); launch / observability on Webflow's platform (use
  house-site-operate-webflow); cross-stack motion (use
  house-site-design-motion); Figma-tool integration when Webflow
  Variables sync isn't feasible (use house-site-design-figma);
  composing this overlay with a per-team overlay (deferred per
  ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, stack-overlay]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 stack-
            overlay batch (Webflow × 3). Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-design-webflow

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay encoding Webflow's design-system + motion conventions
on top of the `site-design` family's mechanism atoms.

## Purpose

Encode how design tokens, components, and motion flow through a
Webflow project:

1. Design tokens use **Webflow Variables** as the platform-native
   source of truth. Where the project also runs Figma + Tokens
   Studio upstream, sync uses the Webflow Variables API
   (limited; not all token types round-trip).
2. The design system lives as **Webflow Components** with variants
   for state.
3. Motion uses **Webflow's native interactions** for simple cases
   and **GSAP via custom-code embed** for cinematic / complex
   timelines.
4. Component states matrix is rendered on a `style-guide` page; not
   all 9 states map cleanly to Webflow's component-variant model
   (notably `loading` / `skeleton` are awkward).
5. Engineering handoff is unusual — Webflow IS the engineering
   surface for the visual layer. The handoff document covers
   custom-code embeds, Logic flows, and CMS schema only.

## Applies On Top Of

- `design-tokens-author` — emits Webflow Variables import format
  rather than DTCG JSON; documents the round-trip gaps with Tokens
  Studio.
- `design-system-author` — Webflow Components + variants; Style
  Guide page is the rendered system.
- `motion-language-author` — Webflow Interactions for simple cases;
  GSAP custom-code embed for cinematic.
- `engineering-handoff-spec-author` — handoff scope reduced
  (Webflow handles most of what would be engineering output);
  covers custom-code embeds + Logic flows + CMS schema.
- `component-states-matrix-author` — variant-based; some states
  (loading, skeleton) flagged as "platform doesn't model cleanly."

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Tokens — Webflow Variables

- **Webflow Variables** are the source of truth for tokens within
  the platform; they map to CSS custom properties at publish time.
- **Color / size / typography** are first-class variable types.
- **Motion duration / easing** are NOT first-class — encoded as
  named utility classes or custom-code-injected CSS variables.
- **Tokens Studio → Webflow** sync: limited. The Webflow Variables
  API allows import but not round-trip for all types. Document the
  gap in the design system.
- **Hand-coded `:root`-injected CSS variables** are forbidden —
  always use Webflow Variables (the platform compiler will conflict
  otherwise).

### Components

- **Webflow Components** for all reusable UI (Hero, Card, Footer,
  Navigation, etc.).
- **Variants** for state changes (default / hover / disabled / etc.);
  the variant slot is the closest analogue to other stacks' state
  matrix.
- **Component naming**: `<Section>/<Component>` (slash-separated)
  for Designer organization; e.g., `Marketing/Hero`,
  `Forms/Newsletter Signup`.
- **Properties** for per-instance customization; prefer over
  hand-edits.

### Motion stack

| Use case | Mechanism |
|---|---|
| Simple reveal / hover / scroll-triggered fade | **Webflow Interactions** (visual editor) |
| Cinematic timelines, scroll-jacked sequences, custom easings | **GSAP custom-code embed** with `<head>` script |
| Page-load reveal sequences | Webflow Interactions on element load |
| Scroll-driven 3D / WebGL hero | **Three.js custom-code embed** + per-page `<head>` initialization (rare; runs into platform's custom-code budget) |

- **GSAP** is loaded via the Webflow CDN-cached custom-code embed
  (use the same script tag site-wide).
- **Custom-code budget**: the platform caps custom code at ~50 KB
  per page; GSAP + ScrollTrigger ~70 KB gz already exceeds this for
  some pages, so loading from CDN is mandatory.
- **Webflow + Lenis**: known incompatibility with Webflow
  Interactions (both hijack scroll events); use one OR the other,
  not both.

### Component states matrix (with Webflow gaps)

| State | Webflow support |
|---|---|
| default | ✅ Component default variant |
| hover | ✅ Variant or built-in `:hover` style |
| focus-visible | ✅ Variant or `:focus-visible` style (selector requires custom CSS) |
| active | ✅ `:active` style |
| disabled | ✅ Variant or attribute selector |
| loading | ⚠️ No native model — combine with custom-code state injection |
| error | ⚠️ Form errors only via Webflow Forms; component-level error needs Logic + custom code |
| empty | ⚠️ CMS empty-state via `Empty State` view; component-level via variant + Logic |
| skeleton | ⚠️ No native model — implement with CSS animation in a variant |

The conformance-statement-author should explicitly list the four
"⚠️" states as known platform gaps the team accepts.

### Style Guide page

- A live `/style-guide` page rendered with every Webflow Component
  in default + key variants.
- Updated as part of every Component change; it's the design-review
  surface (Webflow's analogue to Storybook).

## Override Behavior

This overlay applies when:

- The project ships on Webflow.
- All five mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

The four ⚠️ component states (loading / error / empty / skeleton)
are platform-level gaps; they are NOT overridden — the conformance-
statement explicitly lists them as known platform limitations the
project accepts.

The hand-coded `:root` CSS variables ban is **non-overridable**:
the Webflow compiler conflicts with self-injected variables.

For multi-stack projects (a Webflow marketing site + a code-first
app shell on another stack), use `house-site-design-motion` for
shared motion conventions and ride this overlay only on Webflow
surfaces.

Cross-cutting concerns defer to dedicated atoms per A62 anti-trigger
fallback. See `house-site-design-nextjs` for the canonical list.

## See Also

- `house-site-build-webflow` — SRS / ADR / schedule / runbook /
  threat-model conventions for Webflow.
- `house-site-operate-webflow` — launch + observability conventions
  for Webflow.
- `house-site-design-figma` — when the project ALSO uses Figma
  upstream (with the documented Tokens Studio sync limitations).
- `house-site-design-motion` — cross-stack motion conventions.
- `house-site-design-a11y` — cross-stack a11y conventions.
- `docs/research/E3-technical-conventions.md` §6 (tooling — though
  Webflow is light in the corpus since Awwwards-SOTD overlap is
  thin).
