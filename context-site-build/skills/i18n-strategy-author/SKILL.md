---
name: i18n-strategy-author
description: >
  Authors the i18n (internationalization) strategy specification for
  a site/web-app project. Writes docs/i18n-spec.md covering locale
  routing (sub-path vs domain vs sub-domain), RTL strategy, CSS
  Logical Properties discipline, translation-memory tool selection
  (Crowdin / Lokalise / Phrase / Smartling), CMS locale config, and
  the locale-fallback chain. Free-standing atom outside any family.
  Do NOT use for: actual translation production (translators do that;
  this atom defines the framework); per-component translation strings
  authoring (out of library scope — content lives in the CMS or
  translation-memory tool); legal-jurisdiction / GDPR-region
  considerations (those belong to a future privacy / compliance
  atom; the user-invocable draft-privacy-policy covers that aspect).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [cross-cutting, i18n]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.6.0 Phase 5 cross-
            cutting-tools batch. Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 5; user
            explicitly approved maximalist scope on 2026-05-08.
---

# i18n-strategy-author

> **pre-trigger build (v0.6.0)**; reassess when first consumer
> ships in a multi-locale market triggering the codified strategy
> per `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 5.

Free-standing atom that produces the i18n strategy document
covering routing, RTL, translation tooling, and CMS locale config.
Output: `docs/i18n-spec.md`. The document considers the legal-
jurisdiction and GDPR-region content concerns from a tooling angle
(actual privacy / compliance work belongs to a separate atom). The
i18n strategy applies across all five stack combos.

The atom belongs outside the family roster. Internationalization
compliance considerations and content GDPR-region work are out of
scope (legal-jurisdiction concerns belong to a separate atom). The
web-app i18n-spec lives at `docs/i18n-spec.md`.

## When to Use

- Phase 1 Discovery: when target markets span multiple languages
  and the localization strategy needs scoping.
- Phase 2 Requirements: when SRS NFRs cite multi-language as a
  hard constraint (legal / regulatory / contractual).
- Phase 3 Design: when the design system needs RTL support and
  the CSS Logical Properties discipline must be baked in from
  Day 1.
- Phase 5 Hardening: when adding a second locale to a single-locale
  site post-launch (the most expensive timing — but documented
  here for completeness).
- Adding a new locale to an existing localized site: this atom
  documents the per-locale checklist.

## When NOT to Use

- For per-string translation production — translators / TMS tools
  do that. This atom defines the framework; the strings flow
  through the chosen TMS.
- For privacy / GDPR per-jurisdiction — out of library scope; the
  user-invocable `draft-privacy-policy` covers that aspect.
- For SEO hreflang configuration in isolation — that's part of
  this atom's "locale routing" capability, but if the project's
  primary concern is hreflang and nothing else, fold into
  `srs-author` NFRs rather than authoring a full i18n spec.
- For per-component translation key naming — that's a per-stack
  convention covered in the `house-site-design-{stack}` overlays.

## Capabilities Owned

1. **Locale routing strategy** — sub-path (`/en/`, `/fr/`,
   `/ja/`) vs sub-domain (`fr.example.com`) vs separate-domain
   (`example.fr`) — with the SEO + CDN + cookie-scope tradeoff
   table.
2. **Locale-fallback chain** — `en-GB` → `en` → `default`; per-
   string fallback when the requested locale lacks a translation.
3. **RTL strategy** — when RTL languages (Arabic, Hebrew, Persian,
   Urdu) are in scope; the design-system implications; the
   testing matrix.
4. **CSS Logical Properties discipline** — `margin-inline-start`
   over `margin-left`; `padding-block` over `padding-top`; etc.
   Applies to all stacks; enforced via stylelint rule.
5. **Translation-memory tool selection** — Crowdin (open-source-
   friendly), Lokalise (developer-friendly with API), Phrase
   (enterprise), Smartling (translator-first); per-tool pros/cons
   + CMS integration matrix.
6. **CMS locale config** — Sanity (`@sanity/document-internationalization`),
   Storyblok (built-in i18n), Webflow CMS (limited; per-locale
   collections), Hygraph (built-in localization).
7. **Per-locale launch checklist** — translation completeness gate,
   QA pass, hreflang verification, sitemap-per-locale generation,
   CDN cache strategy.

## Handoffs to Other Skills

- **From `srs-author`** — SRS's "Localization NFRs" section cites
  this document.
- **From `vision-author` / `persona-author`** — when the target
  audience is multi-locale, the discovery atoms cite this
  document.
- **From `adr-author`** — translation-memory tool selection ADR
  cites this document's tool matrix.
- **To `aeo-schema-author`** — Schema.org structured data
  references this document for the `inLanguage` discipline +
  hreflang.
- **To `house-site-design-{nextjs,nuxt,astro,sveltekit,webflow}`**
  — per-stack overlays cite this document for the i18n library
  selection per stack (next-intl / @nuxtjs/i18n / astro-i18n /
  svelte-i18n / Weglot).
- **To `house-site-operate-{vercel,cloudflare,netlify}`** — host
  overlays cite this document for the per-locale CDN edge
  configuration.

## Edge Cases

- **Single-locale site** (default): this atom does not apply; the
  document is not authored. The SRS still mentions
  internationalization-readiness if a future locale is anticipated.
- **Two-locale site with one being a tiny variant** (en-US +
  en-CA): sub-path routing typically; the strategy is brief.
- **20+ locales**: the spec is heavy; CMS choice + TMS tool become
  load-bearing; the per-locale launch checklist is rigorous.
- **Mixed-RTL site** (en + ar simultaneously): the design system's
  Logical Properties discipline + per-component RTL test case is
  load-bearing; visual-regression must include both modes.
- **Legacy site adopting i18n**: the highest-cost path; document
  the migration plan + the breaking-change boundary.

## References

No external `references/*.md` files yet — first real authoring run
will produce templates worth promoting (locale-routing comparison,
RTL strategy, TMS comparison + per-stack SDK availability). Per
the v0.7.0 speculative-skill convention, the absence is flagged
here rather than papered over.
