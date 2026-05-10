# Art Direction — `<project>` (anonymized example output)

> **Note**: anonymized illustrative output of `art-direction-author`.
> Cites `mood-board.md` (which captures the upstream references)
> and produces commitments that constrain Phase 3-7.

---

## The single sentence

Authoritative editorial restraint with one cinematic moment.

---

## Palette

### Brand

| Token | Hex | Use |
|---|---|---|
| `color/brand/primary` | `#0A0A0A` | The single brand color. Black on white; everything's tested against this. |
| `color/brand/accent` | `#FF4D00` | Reserved for the cinematic moment + the primary CTA only. Never decorative. |

### Neutrals

| Token | Hex | Use |
|---|---|---|
| `color/neutral/0` | `#FFFFFF` | Background |
| `color/neutral/100` | `#F5F5F5` | Subtle background variation |
| `color/neutral/200` | `#E0E0E0` | Borders, dividers |
| `color/neutral/500` | `#737373` | Secondary text |
| `color/neutral/700` | `#404040` | Primary text |
| `color/neutral/900` | `#0A0A0A` | Aliased to `color/brand/primary` |

### State

| Token | Hex | Use |
|---|---|---|
| `color/state/success` | `#10B981` | Form success; minimal use |
| `color/state/error` | `#EF4444` | Form error; minimal use |
| `color/state/warning` | `#F59E0B` | Reserved |

**Total brand palette: 2 colors + 6 neutrals + 3 state.** No
gradients except the cinematic moment. No tertiary brand colors.

---

## Typography

### Display

`Söhne` (commercial license per ADR-0011) — display + body.

| Token | Family | Weight | Size | Line | Use |
|---|---|---|---|---|---|
| `type/display/xl` | Söhne | 600 | 96px | 0.95 | Hero only |
| `type/display/l` | Söhne | 600 | 64px | 1.0 | Section heads |
| `type/display/m` | Söhne | 600 | 40px | 1.05 | Sub-section |
| `type/display/s` | Söhne | 500 | 28px | 1.1 | Card heads |

### Body

| Token | Family | Weight | Size | Line | Use |
|---|---|---|---|---|---|
| `type/body/m` | Söhne | 400 | 16px | 1.5 | Body |
| `type/body/s` | Söhne | 400 | 14px | 1.4 | Caption |

### Mono

`JetBrains Mono` — code + the timestamp + numerical accent.

| Token | Family | Weight | Size |
|---|---|---|---|
| `type/mono/m` | JetBrains Mono | 400 | 14px |

---

## Motion vocabulary

Cite `motion-language.md`. Headline commitments here:

- **Page transitions**: instant. No fade-in on the body content.
- **One cinematic moment** per session: the hero scroll-driven 3D
  scene on the homepage. Everywhere else: motion is restrained
  (≤200ms ease-out + opacity).
- **`prefers-reduced-motion`**: hard-disable parallax, smooth-scroll,
  and the cinematic moment. The cinematic moment falls back to a
  static image (per `motion-conformance.md` lite-mode pattern).
- **Hover states**: 100ms color-only transitions. No size changes.
  No shadow elevation. No rotation.
- **Custom cursor**: 8px solid `color/brand/accent` dot tracking the
  pointer. Disabled on touch + on `prefers-reduced-motion`.
  Focus-visible parity preserved (system focus ring NOT replaced).
- **Loading**: skeleton shimmer at `motion-duration-slow` (400ms);
  no spinners.

---

## Photography brief

- **Shot list**: portraits in natural light; no posed studio
  photography; environmental context preserved.
- **Composition**: rule of thirds; subject-left; negative space on
  the right for type overlay.
- **Color grading**: warm-neutral; medium contrast; preserved skin
  tones; no extreme saturation.
- **DPI / format**: 2x retina at delivered size; AVIF + WebP +
  JPEG fallback; LCP-poster image preloaded with `fetchpriority=
  "high"`.
- **Aspect ratios**: 4:5 portrait (above-fold); 16:9 landscape
  (case-study interiors); 1:1 square (grid views).
- **Reference**: see `mood-board.md` Lookbook 3 + 7 + 11.

---

## Layout primitives

Cite `design-system.md`. Headline commitments:

- **Grid**: 12-column desktop with 24px gutter; 4-column tablet
  with 16px gutter; flow-stacked mobile.
- **Container max-width**: 1440px desktop; aligned-center.
- **Vertical rhythm**: 8px base; section padding 96px desktop /
  64px tablet / 40px mobile.
- **Type scale**: modular at 1.25 desktop / 1.2 mobile.

---

## What's deliberately absent

The art-direction is as much about *what we don't do* as what we
do:

- **No drop shadows.** Borders + spacing carry the elevation work.
- **No icon-decorations.** The single accent color does the
  hierarchy.
- **No gradients** outside the cinematic moment.
- **No background images** behind body content.
- **No badges.** Counts and statuses use type-scale variation.
- **No "playful" components** (mascots, illustrations, hand-drawn
  elements). The brand is restrained-editorial.

---

## The cinematic moment

The exception. On the homepage, the scroll-driven 3D scene runs
for the first 3 vertical viewports of scroll. Spec:

- **Stack**: R3F + drei + GSAP ScrollTrigger via `@14islands/r3f-
  scroll-rig` per `house-site-design-nextjs`.
- **Asset**: 1 glTF scene; 18 MB raw → 2.4 MB shipped via Draco +
  KTX2 per `house-site-design-figma` pipeline.
- **Frame budget**: 16ms p95 desktop / 33ms p95 mobile (30fps
  acceptable on mobile).
- **`prefers-reduced-motion`**: replaces with the LCP-poster image;
  scroll behavior is native.
- **Reduced-data**: same lite-mode replacement.
- **A11y**: canvas has `aria-hidden="true"` + `role="presentation"`;
  the scene is decorative; the textual content overlaying the
  canvas is the load-bearing content.

---

## Authority

- Mood board: `mood-board.md` v0.3 (2026-04-26).
- Vision: `vision.md` v0.2 (2026-04-23).
- Persona: `personas.md` v0.1 (3 personas).
- Concept: `concept.md` v0.1 (creative territory + lore).

## Sign-off

| Role | Name | Date |
|---|---|---|
| Creative Director | `<anonymized>` | 2026-04-30 |
| Founding team | `<anonymized>` | 2026-05-01 |

---

## Cross-references

- `motion-language.md` — motion vocabulary detailed.
- `design-tokens-author` output — palette + type tokens emitted as
  DTCG JSON.
- `design-system.md` — components built against this art-direction.
- `engineering-handoff-spec.md` — handoff cites this document by
  section number.

---

*Authored 2026-04-29 by art-direction-author v0.1.0. Sign-off: 2026-
05-01.*
