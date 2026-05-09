---
name: motion-conformance-author
description: >
  Authors the motion-conformance specification covering WCAG 2.2
  motion criteria (2.1.1 keyboard / 2.2.2 pause-stop-hide / 2.3.3
  animation-from-interactions / 2.4.7 focus-visible / 2.5.7 dragging-
  movements / 2.5.8 target-size). Writes docs/05-hardening/motion-
  conformance.md plus the axe-core CI configuration and the manual
  keyboard / screen-reader test plan. Codifies three flavours of
  prefers-reduced-motion (hard-disable / soft-degrade / alternative-
  experience), focus-visible parity for custom cursors, keyboard-on-
  scroll-jacked patterns, and the lite-mode alternative experience.
  Free-standing atom outside any family. Do NOT use for: per-component
  a11y annotations (use a11y-annotations-author); WCAG-EM conformance
  statement at Phase 5 close (use conformance-statement-author —
  this atom feeds into it); design-system motion library selection
  (use motion-language-author); cross-stack motion conventions (use
  house-site-design-motion or house-site-design-a11y — this atom is
  the cross-cutting tool both reference).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [cross-cutting, a11y, weekly]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.6.0 Phase 5 cross-
            cutting-tools batch. Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 5; user
            explicitly approved maximalist scope on 2026-05-08.
---

# motion-conformance-author

> **pre-trigger build (v0.6.0)**; reassess when first consumer hits
> a motion-a11y crisis triggering the codified conformance
> per `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 5.

Free-standing atom that produces the motion-conformance document
+ the axe-core CI configuration + the manual test plan. Not in any
family — applies across the site-build / site-design / site-operate
methodology and across all 5 stack combos.

## When to Use

- Phase 3 Design: when the motion-language is being authored and
  needs the WCAG 2.2 conformance constraints baked in.
- Phase 5 Hardening: when CI gates need axe-core + the manual test
  plan is being scheduled.
- Phase 5 a11y conformance attestation: this document feeds into
  `conformance-statement-author`'s WCAG-EM statement.
- Pre-launch motion-heavy site: when the team needs to know what
  ships and what's deferred to v1.1 because of conformance gaps.

## When NOT to Use

- For per-component a11y annotations (alt text, ARIA, role) — use
  `a11y-annotations-author`.
- For the WCAG-EM-flavored conformance statement — use
  `conformance-statement-author` (which cites this document).
- For the design-system motion library + token spec — use
  `motion-language-author`.
- For the operate-overlay's CI integration commands — those go in
  `house-site-operate-{vercel,cloudflare,netlify}` (which cite
  this document).

## Capabilities Owned

1. **WCAG 2.2 motion-criteria coverage table** — criterion-by-
   criterion (2.1.1 / 2.2.2 / 2.3.3 / 2.4.7 / 2.5.7 / 2.5.8) with
   the typical Awwwards-tier failure mode + the project's
   commitment per criterion.
2. **Three prefers-reduced-motion patterns** — hard-disable / soft-
   degrade / alternative-experience with per-pattern when-to-use
   guidance.
3. **Focus-visible parity for custom cursors** — the patterns that
   keep focus visible alongside or via the custom cursor.
4. **Keyboard scroll bindings** — ArrowDown / PageDown / Space
   bound to chapter navigation when ScrollSmoother / Lenis is
   active; Lenis destroyed on `prefers-reduced-motion: reduce`.
5. **Lite-mode alternative experience** — `/lite` URL, `?lite=1`
   query, or `prefers-reduced-data` UA hint; HTML-only hero, native
   scroll, search-engine-indexable.
6. **axe-core CI configuration** — `.axe-core.json` or framework-
   specific equivalent (Storybook addon, Histoire addon, Playwright
   E2E suite).
7. **Manual test plan** — keyboard-only navigation, VoiceOver +
   NVDA passes, high-contrast / forced-colors pass, color-contrast
   measurement schedule.
8. **Honest disclaimer** — automated tooling catches ~30-40% of
   real WCAG 2.2 barriers (per E3 §4.4); the conformance statement
   reflects this honestly.

## Handoffs to Other Skills

- **From `motion-language-author`** — motion-language's prefers-
  reduced-motion section cites this document for the patterns +
  the WCAG mapping.
- **From `srs-author`** — SRS's "Accessibility NFRs" section cites
  this document by URL/section.
- **To `conformance-statement-author`** — the Phase-5 conformance
  statement reads this document's coverage table + the axe-core CI
  results + the manual test results to compose the WCAG-EM
  statement.
- **To `a11y-annotations-author`** — per-component annotations cite
  this document's component-level patterns (focus-visible parity
  in particular).
- **To `house-site-design-a11y`** — the cross-stack a11y overlay
  cites this document for the project-level conformance posture.
- **To `house-site-operate-{vercel,cloudflare,netlify}`** —
  hosting-specific operate-overlays cite this document for the
  axe-core CI integration command.

## Edge Cases

- **Site is fully static + motion-light**: most criteria are auto-
  satisfied; the document still ships but the manual test plan is
  abbreviated.
- **Site is cinematic / scrolly-telling-heavy**: the lite-mode
  alternative-experience path becomes load-bearing; the document
  details the lite-mode content audit.
- **Site mixes motion-heavy hero with static body**: per-page
  conformance statements; the document's coverage table applies
  per page-type.
- **Conformance gaps the team consciously ships**: documented in
  the conformance statement with WCAG criterion + rationale +
  remediation timeline; this atom does NOT enforce 100% coverage,
  it documents what's covered and what's deferred.
- **`prefers-reduced-data` is set but `prefers-reduced-motion` is
  not**: edge — the project's lite-mode trigger logic should fire
  on either; the document specifies the OR'd condition.

## References

- `references/wcag-coverage-table.md` — the criterion-by-criterion
  table with failure modes + commitments + axe-core test mapping.
- `references/reduced-motion-patterns.md` — the three patterns
  with per-pattern code examples for the 5 stack combos (covered
  via `house-site-design-motion` per-stack overlays as
  cross-references).
- `references/manual-test-plan.md` — keyboard / screen-reader /
  forced-colors / contrast schedule + tooling.
