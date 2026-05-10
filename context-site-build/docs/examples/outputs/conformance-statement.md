# WCAG 2.2 Conformance Statement — `<project>` (anonymized example)

> **Note**: anonymized illustrative output of `conformance-statement-
> author`. Reads `motion-conformance.md` + axe-core CI results +
> manual test results. This document is the WCAG-EM-flavored
> attestation that ships with the v1.0 launch.

---

## Conformance level

`<project>` conforms to **WCAG 2.2 Level AA** for all surfaces, with
specific exceptions documented per criterion below.

**Audit date**: 2026-05-09 (v1.0 launch).
**Re-audit cadence**: every 6 months OR with each MAJOR release.
**Method**: axe-core automated CI + manual keyboard test + manual
screen-reader test (VoiceOver macOS, NVDA Windows) + high-contrast
+ forced-colors mode pass.

---

## Honest disclaimer

Per `motion-conformance.md` § "Automated-tooling honesty":
**axe-core catches ~30–40% of real WCAG 2.2 barriers** (cited from
E3 §4.4 in our research base). The remaining 60–70% requires
manual testing. Below, we document which criteria axe-core covers
+ which we tested manually.

---

## Per-criterion attestation (WCAG 2.2 AA + relevant AAA)

### Perceivable

| Criterion | Level | Conformance | Method | Notes |
|---|---|---|---|---|
| 1.1.1 Non-text Content | A | ✅ Pass | axe + manual | All images have alt; decorative canvas has `aria-hidden="true"` |
| 1.3.1 Info & Relationships | A | ✅ Pass | axe + manual | Semantic HTML; ARIA where needed |
| 1.3.2 Meaningful Sequence | A | ✅ Pass | manual | Reading order verified per page |
| 1.4.3 Contrast (Minimum) | AA | ✅ Pass | axe | All text-on-background pairs ≥ 4.5:1 |
| 1.4.4 Resize Text | AA | ✅ Pass | manual | Text resizable to 200% without loss |
| 1.4.10 Reflow | AA | ✅ Pass | manual | 320px viewport reflow verified |
| 1.4.11 Non-text Contrast | AA | ✅ Pass | axe | UI components ≥ 3:1 |
| 1.4.12 Text Spacing | AA | ✅ Pass | manual | User-overridden text spacing tested |
| 1.4.13 Content on Hover/Focus | AA | ✅ Pass | manual | Tooltips dismissable; persistent enough |

### Operable (motion-criteria highlighted)

| Criterion | Level | Conformance | Method | Notes |
|---|---|---|---|---|
| **2.1.1 Keyboard** | A | ✅ Pass | manual | Custom cursor coexists with system focus; cinematic scene has keyboard alternative (lite-mode) |
| 2.1.2 No Keyboard Trap | A | ✅ Pass | manual | All modals/dialogs trap focus correctly + offer Esc |
| **2.2.2 Pause, Stop, Hide** | A | ✅ Pass | manual | Global motion toggle in header; hero scene auto-pauses on `prefers-reduced-motion` |
| **2.3.3 Animation from Interactions** | AAA | ⚠ Partial | manual | `prefers-reduced-motion` honored; not all sub-motions individually pause-able |
| 2.4.1 Bypass Blocks | A | ✅ Pass | manual | Skip-to-main-content link |
| 2.4.3 Focus Order | A | ✅ Pass | manual | Logical tab order verified |
| 2.4.4 Link Purpose (in Context) | A | ✅ Pass | axe | All links have meaningful text |
| **2.4.7 Focus Visible** | AA | ✅ Pass | manual | System focus ring preserved alongside custom cursor |
| 2.5.1 Pointer Gestures | A | ✅ Pass | manual | All pointer-driven actions have button equivalents |
| 2.5.2 Pointer Cancellation | A | ✅ Pass | manual | All up-pointer actions cancellable |
| 2.5.3 Label in Name | A | ✅ Pass | axe | Accessible names match visible labels |
| 2.5.4 Motion Actuation | A | ✅ Pass | manual | No motion-actuated controls |
| **2.5.7 Dragging Movements** (NEW 2.2) | AA | ✅ Pass | manual | Image-grid reordering has button-based alternative; cart-style drag-to-add (N/A, no cart) |
| **2.5.8 Target Size (Minimum)** (NEW 2.2) | AA | ✅ Pass | axe + manual | All interactive targets ≥ 24×24 CSS px verified |

### Understandable

| Criterion | Level | Conformance | Method | Notes |
|---|---|---|---|---|
| 3.1.1 Language of Page | A | ✅ Pass | axe | `<html lang="en">` |
| 3.2.1 On Focus | A | ✅ Pass | manual | Focus does not trigger context change |
| 3.2.2 On Input | A | ✅ Pass | manual | Form input doesn't trigger context change without warning |
| 3.2.6 Consistent Help (NEW 2.2) | A | ✅ Pass | manual | Help section in same location across pages |
| 3.3.1 Error Identification | A | ✅ Pass | axe + manual | Form errors announce via `aria-describedby` |
| 3.3.3 Error Suggestion | AA | ✅ Pass | manual | Suggested corrections offered where computable |
| 3.3.7 Redundant Entry (NEW 2.2) | A | ✅ Pass | manual | No redundant entry across signup flow |
| 3.3.8 Accessible Authentication (NEW 2.2) | AA | ✅ Pass | manual | Email + password (WCAG-acceptable; password manager support) |

### Robust

| Criterion | Level | Conformance | Method | Notes |
|---|---|---|---|---|
| 4.1.2 Name, Role, Value | A | ✅ Pass | axe + manual | All interactive components have accessible name + role + state |
| 4.1.3 Status Messages | AA | ✅ Pass | manual | Toasts announce via `aria-live="polite"` |

---

## Known gaps (the honest caveat)

### 2.3.3 Animation from Interactions (AAA — partial)

The cinematic homepage scene has multiple sub-motions
(geometry rotations, scroll-driven camera moves, particle
animations). Currently:

- The whole scene pauses when `prefers-reduced-motion: reduce`.
- The lite-mode alternative experience (per `motion-conformance.md`)
  provides a static fallback.
- **NOT YET**: per-sub-motion pause control. The user cannot pause
  particle animations independently of camera animations.

This is a 2.3.3 AAA concern (not AA-blocking). Tracked as
`<issue-id>` for v1.1 consideration.

### Voice-control passes

We tested keyboard + screen-reader. We did **not** test voice-
control (Voice Control on macOS / Voice Access on Android). For v1.0,
voice-control is a known untested surface; report received: works
for basic navigation, untested on the cinematic scene. Tracked as
`<issue-id>` for v1.1 testing.

---

## Test methodology

### Automated tests (axe-core CI)

- Runs on every preview deploy via `@axe-core/playwright`.
- Fails the build on any **serious** or **critical** violation.
- Configuration: `axe-core.config.json`.
- Results dashboard: `<sentry-or-equivalent-dashboard-URL>`.

### Manual keyboard pass

- Tab through every interactive element on each page.
- Verify focus indicator visible at all times.
- Verify all functions reachable + operable via keyboard.
- Performed by: `<anonymized-tester>` on 2026-05-08.

### Manual screen-reader pass

- VoiceOver (macOS Sonoma) — Safari + Chrome.
- NVDA (Windows 11) — Firefox + Chrome.
- Test scenarios: signup, edit portfolio, publish, view published
  site, contact form.
- Performed by: `<anonymized-tester>` on 2026-05-08.

### High-contrast / forced-colors pass

- Windows High Contrast (Aquatic theme).
- macOS Increase Contrast.
- All UI remains usable; brand colors substituted with system
  colors per `forced-colors: active` media query.

### Color-contrast measurement

- WebAIM Contrast Checker against every text-on-background pair.
- Min ratio observed: 4.6:1 (`color-neutral-500` body on
  `color-neutral-100` subtle bg).

---

## Escalation + remediation

If a user reports an accessibility issue:

1. Email `<accessibility-contact-email>`.
2. Triage within 5 business days.
3. Fix timeline:
   - **Critical** (blocks core functionality): patched within 7 days.
   - **Serious**: within 30 days.
   - **Moderate**: next regular release.

A signed Statement of Effort (per `<a11y-policy>`) is available
upon request.

---

## Authority

- WCAG 2.2 Recommendation (W3C, October 2023).
- Motion conformance: `motion-conformance.md` v0.1.
- A11y annotations per component: `a11y-annotations.md` v0.1.
- Cross-stack overlay: `house-site-design-a11y`.

---

*Authored 2026-05-09 by conformance-statement-author v0.1.0. Manual
testing performed 2026-05-08 by `<anonymized>`. Statement reviewed
+ approved 2026-05-09. Re-audit due 2026-11-09.*
