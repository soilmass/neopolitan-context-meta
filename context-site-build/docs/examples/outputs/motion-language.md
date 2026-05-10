# Motion Language — `<project>` (anonymized example output)

> **Note**: anonymized illustrative output of `motion-language-
> author`. Cites `art-direction.md` (which establishes restraint
> + the cinematic-moment exception) and `house-site-design-motion`
> (which provides the cross-stack motion conventions).

---

## Posture

Per `art-direction.md` § Motion vocabulary: **restrained-editorial
with one cinematic moment**. Motion is feedback, not décor —
except for the homepage hero, where motion *is* the message.

Per IBM Carbon's motion taxonomy: this project is **expressive**
on the homepage hero; **productive** everywhere else.

---

## Motion tokens

Emitted as DTCG JSON via `design-tokens-author` per
`house-site-design-figma` pipeline. CSS variables + Tailwind v4
`@theme` block + TypeScript types.

### Duration

| Token | Value | Use |
|---|---|---|
| `motion-duration-fast` | 100ms | Hover states; immediate feedback |
| `motion-duration-medium` | 200ms | Tooltip / popover enter; default UI |
| `motion-duration-slow` | 400ms | Skeleton shimmer; modal enter |
| `motion-duration-very-slow` | 800ms | Reserved (rarely used) |

### Easing

| Token | Bezier | Use |
|---|---|---|
| `motion-ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Default; emphasized end |
| `motion-ease-in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` | Symmetric; reserved |
| `motion-ease-emphasized` | `cubic-bezier(0.05, 0.7, 0.1, 1)` | Layout shifts |
| `motion-ease-bounce` | `cubic-bezier(0.68, -0.55, 0.265, 1.55)` | Reserved (NOT used; placeholder) |

### Distance

| Token | Value | Use |
|---|---|---|
| `motion-distance-1` | 8px | Standard hover offset |
| `motion-distance-2` | 16px | Modal enter slide |
| `motion-distance-3` | 24px | Reserved |

---

## Library selection (per `house-site-design-motion` table)

| Use case | Library | Notes |
|---|---|---|
| Marketing hero scroll-driven scene (the cinematic moment) | **GSAP + ScrollTrigger** + `@14islands/r3f-scroll-rig` (Lenis under the hood) | The single use of cinematic motion |
| App-shell UI (auth-required surfaces) | **Motion (Framer Motion)** | Layout transitions, exit animations |
| Hover states everywhere | Native CSS transitions (no library) | 100ms color-only |
| Loading states | CSS-keyframe shimmer | No library; no JS |
| Page transitions | None | Instant; no fade |

GSAP + ScrollTrigger is loaded only on the homepage route. Motion
is loaded only on auth-required routes. Hover/loading are zero-JS.

---

## Scene scoping discipline (per `house-site-design-motion`)

The homepage hero scene is the only scene. Pattern:

```tsx
// app/(marketing)/page.tsx — RSC parent
import { HomepageHero } from '@/components/marketing/HomepageHero'

export default function HomePage() {
  return (
    <main>
      <HomepageHero />
      <RestOfPageRSC />
    </main>
  )
}

// components/marketing/HomepageHero.tsx — client island
'use client'

import { useGSAP } from '@gsap/react'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { Canvas } from '@react-three/fiber'
import { ScrollControls, useScroll } from '@react-three/drei'

export function HomepageHero() {
  const ref = useRef<HTMLDivElement>(null)

  useGSAP(() => {
    // Scene scoping: gsap.context-equivalent via useGSAP
    // ScrollTrigger registered + cleaned up in scope
    ScrollTrigger.create({ /* ... */ })
  }, { scope: ref })

  return (
    <div ref={ref}>
      <Canvas>
        <ScrollControls pages={3} damping={0.25}>
          {/* scene */}
        </ScrollControls>
      </Canvas>
    </div>
  )
}
```

Per the scope: scene unmounts cleanly on route change; ScrollTrigger
instances revert; no stale listeners.

---

## `prefers-reduced-motion` handling (per `motion-conformance.md`)

Three patterns documented; this project uses **all three** at
different layers:

### Hard-disable (decorative motion)

The cinematic homepage scene + Lenis smooth-scroll:

```css
@media (prefers-reduced-motion: no-preference) {
  /* Lenis applied */
  html { scroll-behavior: smooth; }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  /* Lenis JS not initialized; native scroll only */
}
```

The scene itself is replaced with the LCP-poster image; canvas not
rendered; no GSAP timelines.

### Soft-degrade (UI feedback motion)

Modal enters, tooltips, popovers:

```tsx
// motion.dev (Framer Motion) variant
const reduced = useReducedMotion()
<motion.div
  initial={{ opacity: 0, y: reduced ? 0 : 16 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: reduced ? 0.1 : 0.2 }}
/>
```

Movement removed; opacity preserved at 100ms.

### Alternative experience (lite-mode)

Per `motion-conformance.md`: a `/lite` route OR `?lite=1` query
triggers the alternative. For the homepage, the cinematic scene is
replaced with the static LCP-poster + the textual content. The lite
route is search-engine-indexable (no `noindex`).

---

## Focus-visible parity (per `house-site-design-a11y`)

Custom cursor (8px solid `color/brand/accent` dot) coexists with
the system focus indicator. The custom cursor is purely visual; it
does not replace `:focus-visible` rings.

Implementation:

```css
/* System focus indicator preserved */
*:focus-visible {
  outline: 2px solid var(--color-brand-primary);
  outline-offset: 2px;
}

/* Custom cursor disabled on touch + on prefers-reduced-motion */
@media (hover: hover) and (prefers-reduced-motion: no-preference) {
  body {
    cursor: none;
  }
  /* Custom cursor element rendered + tracked */
}
```

---

## Keyboard scroll bindings

Lenis is the smooth-scroll engine on the homepage hero. Per
`house-site-design-a11y`:

- `Space` / `PageDown` → scroll one viewport (default; not
  hijacked).
- `Shift+Space` / `PageUp` → scroll one viewport up.
- `Home` / `End` → top / bottom of page.
- `ArrowDown` / `ArrowUp` → small-step scroll (matches native).

Lenis hijacks wheel + touch only; keyboard events fall through to
native browser handling. No custom keyboard chapter-binding (the
homepage isn't scroll-snap).

---

## Component-level motion

Per `design-system.md` 9-state matrix:

| State | Motion |
|---|---|
| default | None |
| hover | 100ms color transition (`motion-duration-fast` + `motion-ease-out`); no size / shadow changes |
| focus-visible | Instant outline; no transition (focus indicator must be unambiguous) |
| active | Instant; no transition |
| disabled | None |
| loading | `motion-duration-slow` skeleton shimmer; reduced-motion: static gray block |
| error | Instant red border; 200ms shake on form-submit failure (reduced-motion: no shake) |
| empty | None |
| skeleton | `motion-duration-slow` shimmer (same as loading) |

---

## What we deliberately don't animate

- Page transitions (instant).
- Body text reveals on scroll (instant — not the kind of cinematic).
- Card hovers (color-only).
- Modal entry from off-screen (modals fade in; don't slide).
- Anything triggered by scroll except the homepage hero.

---

## Authority

- Art direction: `art-direction.md` v0.1 (sign-off 2026-05-01).
- Design system: `design-system.md` v0.1.
- WCAG criteria: `motion-conformance.md` v0.1.
- Cross-stack overlay: `house-site-design-motion`.

---

*Authored 2026-05-03 by motion-language-author v0.1.0. Reviewed
2026-05-08 by engineering. Sign-off: 2026-05-09.*
