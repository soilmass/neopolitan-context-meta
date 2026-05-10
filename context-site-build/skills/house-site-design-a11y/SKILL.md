---
name: house-site-design-a11y
description: >
  Cross-stack accessibility conventions for motion-heavy sites,
  overlaid on a11y-annotations-author, motion-language-author, and
  component-states-matrix-author. Encodes WCAG 2.2 motion-criteria
  coverage (2.1.1 keyboard / 2.2.2 pause-stop-hide / 2.3.3 animation-
  from-interactions / 2.4.7 focus-visible / 2.5.7 dragging-movements /
  2.5.8 target-size); the three flavours of prefers-reduced-motion
  (hard-disable / soft-degrade / alternative-experience); focus-visible
  parity for custom cursors; keyboard scroll bindings on scroll-jacked
  sites; lite-mode alternative-experience pattern; the honest 30-40%
  automated-tooling caveat. Stack-agnostic. Do NOT use for: motion
  library / token / scene-scoping conventions (use
  house-site-design-motion); stack-specific design conventions (use
  house-site-design-{nextjs,nuxt,astro,sveltekit,webflow}); composing
  this overlay with a per-team overlay (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, cross-stack, a11y]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 cross-
            stack overlay batch. Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
            Pairs with motion-conformance-author (PR #7) — this
            overlay adds the per-component a11y patterns the
            cross-cutting tool atom cannot encode generically.
---

# house-site-design-a11y

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Cross-stack overlay encoding the accessibility conventions that
turn a motion-heavy "Awwwards-tier" site from "shipping a
Reduce-Motion CSS branch and calling it done" (E3 §4.1) into
something the WCAG 2.2 reality respects.

## Purpose

Encode the conventions that close the agency-vs-WCAG gap on motion-
heavy sites:

1. WCAG 2.2 motion-criteria coverage is named criterion-by-criterion
   (2.1.1, 2.2.2, 2.3.3, 2.4.7, 2.5.7, 2.5.8) with the typical
   Awwwards-tier failure mode for each.
2. The three `prefers-reduced-motion` patterns are documented with
   when each applies.
3. Focus-visible parity is mandatory for any custom cursor (the
   single most common failure on Awwwards-tier sites).
4. Keyboard scroll bindings replace hijacked-scroll behavior for
   keyboard / screen-reader users.
5. The "lite-mode alternative experience" pattern provides a non-
   WebGL fallback for users where motion *is* the message.
6. The honest disclaimer: automated tooling catches ~30–40% of
   barriers; manual keyboard + screen-reader testing covers the rest.

## Applies On Top Of

- `a11y-annotations-author` — adds the WCAG 2.2 motion-criteria
  coverage table + the "What axe-core won't catch" honest section.
- `motion-language-author` — adds the three reduced-motion
  patterns + the lite-mode alternative-experience pattern.
- `component-states-matrix-author` — adds focus-visible parity
  requirement for any custom cursor; states matrix gets explicit
  "focus-visible behavior with custom cursor" row.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### WCAG 2.2 motion-criteria coverage (citing E3 §4.4)

| Criterion | What WCAG says | Awwwards-tier reality | This overlay's enforcement |
|---|---|---|---|
| **2.1.1 Keyboard (A)** | All functionality keyboard-accessible | Custom cursors / drag-only interactions break this | Mandatory keyboard alternative for every interaction; documented per component |
| **2.2.2 Pause, Stop, Hide (A)** | Auto-updating motion must have a control | Hero loops rarely have pause control | Global motion toggle in UI (header / footer); persists per-session |
| **2.3.3 Animation from Interactions (AAA)** | Non-essential animation can be disabled | Honored only via `prefers-reduced-motion` for sites that bothered | Mandatory per-feature `prefers-reduced-motion` opt-in |
| **2.4.7 Focus Visible (AA)** | Focus indicator must be visible | Custom cursors often suppress focus rings without replacement | Focus-visible parity mandatory; documented in component states matrix |
| **2.5.7 Dragging Movements (AA, new in 2.2)** | Drag must have a single-pointer alternative | "Drag to explore" interactions almost universally fail | Click / tap / keyboard alternative documented per drag interaction |
| **2.5.8 Target Size Minimum (AA, new in 2.2)** | 24×24 CSS px minimum | Tight cursor-driven UIs frequently fail | Target-size measured at component review |

### The three `prefers-reduced-motion` patterns (citing E3 §4.2)

The opt-in pattern: write base CSS *without* motion, then layer
motion inside `@media (prefers-reduced-motion: no-preference)`.
This makes "no motion" the safe default.

| Pattern | When to use |
|---|---|
| **Hard-disable** | Decorative motion (smooth scroll, parallax, autoplay carousels, hover transitions). Wrap in `@media (prefers-reduced-motion: no-preference) { … }`; static content shown otherwise. The default and only safe approach for purely decorative motion. |
| **Soft-degrade** | Component design systems. Replace large vestibular triggers (full-page swipes, parallax, zoom-in/out) with `opacity` cross-fades. Functional motion (tooltip slide-in) keeps a 100ms version. |
| **Alternative experience** | When the motion *is* the message — cinematic sites, scrolly-telling. Whole alternative content path: a static "lite" version OR a `<noscript>`-style HTML-only hero. |

### Focus-visible parity for custom cursors

- Any custom cursor MUST coexist with the system focus indicator OR
  replace it with an equivalent visual focus signal.
- The `component-states-matrix-author` 9-state matrix gets an
  explicit `focus-visible (with custom cursor)` row — what does
  focus look like when the custom cursor is active?
- Pattern: maintain the system focus ring; the custom cursor is an
  *addition* not a replacement. OR: the custom cursor's shape /
  position changes when an element is focused.

### Keyboard scroll bindings on scroll-jacked sites

Required when `Lenis` or `ScrollSmoother` hijacks wheel/touch:

- **Bind ArrowDown / PageDown / Space → next chapter** via
  ScrollTrigger's `gotoSection(i+1)` or equivalent.
- **Bind ArrowUp / PageUp / Shift+Space → previous chapter**.
- **Bind Home / End → first / last chapter**.
- **Skip-to-chapter link** (`aria-label`-ed) at the top of the page.
- **`prefers-reduced-motion: reduce`** users get native scroll
  back; Lenis is destroyed; sections become normal long-scroll
  columns.

### Lite-mode alternative experience

For sites where the motion *is* the message:

- **`/lite` URL** OR **`?lite=1` query string** OR **`prefers-reduced-
  data` UA hint** triggers the alternative.
- **Alternative content**: HTML-only hero (no canvas, no GSAP),
  static images instead of WebGL, native scroll instead of Lenis.
- **Linked from the global motion toggle** in the UI.
- **Indexed by search engines** the same as the primary experience
  (no `robots: noindex` on the lite path).

### Automated-tooling honesty

- **axe-core CI** (via `@axe-core/playwright` or Storybook addon)
  catches ~30–40% of real WCAG 2.2 barriers (E3 §4.4).
- **Manual audits** cover the rest:
  - Keyboard-only navigation pass (every interactive element
    reachable + operable).
  - Screen-reader pass with VoiceOver (macOS / iOS) + NVDA
    (Windows).
  - High-contrast / forced-colors pass.
  - Color-contrast measurement at every contrast pair.
- **Conformance statement** explicitly names the automated-vs-
  manual split.

## Override Behavior

This overlay applies when:

- The project's `srs-author` output cites motion as load-bearing
  (cinematic site, scrolly-telling, animated marketing hero).
- All three mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

The WCAG 2.2 motion-criteria coverage table is **non-overridable**:
projects that consciously choose to ship without keyboard
alternatives, focus-visible parity, or motion toggles need to do so
with explicit signed-off ADRs documenting the WCAG criteria they
choose to fail and why. The conformance statement reflects this
honestly.

The "axe-core catches 30–40%" disclaimer is **non-overridable**;
projects that claim full WCAG 2.2 compliance via automated tooling
alone are misrepresenting the standard.

WCAG 2.2 motion-criteria conformance enforcement (CI gates,
component-level conformance attestation) defers to
`motion-conformance-author` (PR #7 / v0.6.0). Per A62 anti-trigger
fallback: use `motion-conformance-author`; the user-
invocable `draft-motion-conformance` covers it now.

## See Also

- `house-site-design-motion` — cross-stack motion library + token +
  scene-scoping conventions (this overlay covers the a11y layer).
- `house-site-design-{nextjs,nuxt,astro,sveltekit,webflow}` — per-
  stack design overlays.
- `motion-conformance-author` (deferred to PR #7 / v0.6.0) — the
  cross-cutting tool atom that enforces this overlay's coverage at
  CI level.
- `docs/research/E3-technical-conventions.md` §4 (a11y reality) —
  evidence base.
