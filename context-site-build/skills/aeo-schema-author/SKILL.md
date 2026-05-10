---
name: aeo-schema-author
description: >
  Authors the AEO (Answer Engine Optimization) / SEO Schema.org
  structured-data specification. Writes docs/aeo-schema-spec.md plus
  src/lib/schema/<type>.ts JSON-LD generators per page type
  (Organization / WebSite / Product / Article / FAQ / HowTo +
  others as needed). Codifies AI-search citation discipline +
  Rich Results Test validation + the structured-data CI gate. Free-
  standing atom. Do NOT use for: AEO baseline metrics measurement
  (use aeo-baseline-author — this atom defines the structured-data
  spec; aeo-baseline-author measures whether AI-search engines are
  citing the site); analytics events for AEO conversions (use
  analytics-instrumentation-author); content authoring per page
  (out of library scope — content lives in CMS or Markdown).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [cross-cutting, seo, weekly]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.6.0 Phase 5 cross-
            cutting-tools batch. Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 5; user
            explicitly approved maximalist scope on 2026-05-08.
---

# aeo-schema-author

> **pre-trigger build (v0.6.0)**; reassess when first consumer
> needs codified AEO / structured-data spec per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 5.

Free-standing atom that produces the Schema.org / JSON-LD
structured-data specification + the per-page-type generator
templates. Output: `docs/aeo-schema-spec.md` and the
`src/lib/schema/<type>.ts` generators. The atom covers the AI-search
engine citation-discipline conventions, the Rich Results Test
validation gate, and the AEO baseline measurement metric set.
Applies across the methodology — every page-rendering surface in
any stack combo emits structured data per this spec.

The AEO measurement standards, conversion gating, and validation
optimization patterns are free-standing concerns that compose with
the `aeo-schema-spec` and `aeo-baseline-author`.

## When to Use

- Phase 2 Requirements: when SEO/AEO is named as a load-bearing
  constraint in the SRS.
- Phase 4 Build: when components are being authored and the
  per-component JSON-LD output needs the schema spec.
- Phase 7 Post-launch: when AI-search citation pressure surfaces
  (the project isn't appearing in Perplexity / ChatGPT-search /
  Gemini answers despite ranking on Google) and the spec needs
  codification.
- Marketing or content team requests "make us appear in answer-
  engines" — this atom is the engineering response.

## When NOT to Use

- For measuring AEO outcomes (impression share, citation count,
  click-through from AI-search) — use `aeo-baseline-author`. This
  atom defines the spec; aeo-baseline measures the result.
- For analytics events related to AEO — use
  `analytics-instrumentation-author`.
- For content authoring (the actual product descriptions, FAQs,
  HowTo prose) — out of library scope; content lives in CMS or
  Markdown.
- For per-route URL strategy / canonical / hreflang — those are
  classic SEO concerns covered in `srs-author` NFRs (or a future
  `seo-strategy-author` if dedicated tool needed).

## Capabilities Owned

1. **Per-page-type Schema.org schema** — Organization (root),
   WebSite (root + sitelinks search), Product (e-commerce), Article
   (blog / press), FAQ (FAQ pages), HowTo (tutorial pages),
   BreadcrumbList (navigation), VideoObject (video pages),
   LocalBusiness (when applicable).
2. **JSON-LD generators** — TypeScript functions that produce
   validated JSON-LD given the page's content; Zod-validated to
   match Schema.org shape; emit `<script type="application/ld+
   json">` server-side per the framework.
3. **Rich Results Test integration** — CI step that runs every
   PR's preview deploy through Google's Rich Results Test API +
   Schema.org Validator; fails the build on errors.
4. **AI-search citation discipline** — the conventions that
   maximize Perplexity / ChatGPT-search / Gemini citation
   (clear question-answer structure on key pages; Author /
   datePublished / dateModified properties; canonical URL
   discipline).
5. **AEO baseline metrics** — what to track post-launch so the
   `aeo-baseline-author` atom has a metric set (impression share,
   citation count, click-through).
6. **OpenGraph + Twitter Card mapping** — alongside JSON-LD,
   the per-page-type meta-tag set.

## Handoffs to Other Skills

- **From `srs-author`** — SRS's "SEO/AEO NFRs" section cites this
  document.
- **From `adr-author`** — when a project chooses an unusual
  schema (e.g., `Course` for an online learning platform), the
  ADR documents the rationale.
- **To `aeo-baseline-author`** — Phase-7 baseline reads this
  document's metric set + the spec; measures whether the
  structured data is actually being consumed by AI search.
- **To `analytics-instrumentation-author`** — the AEO-conversion
  events (a search-engine-referred user reaching key pages) are
  defined here as the spec; the events themselves are authored in
  analytics-instrumentation.
- **To components** — every component that renders a page (Hero,
  ProductCard, ArticleHeader, FAQ, HowToStep) imports the
  appropriate `src/lib/schema/<type>.ts` generator.
- **To `house-site-build-{nextjs,nuxt,astro,sveltekit,webflow}`**
  — per-stack overlays cite this atom for the framework-specific
  JSON-LD injection pattern.

## Edge Cases

- **Site is single-page** (microsite, campaign): only Organization
  + WebSite schemas; the document is brief.
- **Site is content-heavy** (publication, blog at scale): the
  Article + Author + datePublished + dateModified discipline is
  load-bearing; CI must enforce.
- **E-commerce with thousands of SKUs**: the Product schema is
  generator-driven (CMS field → schema); Rich Results Test runs
  on a sampled subset (full-product runs are too slow for CI).
- **Multi-language site**: schema includes `inLanguage` per
  document; Cross-references with `i18n-strategy-author` for
  hreflang discipline.
- **AI-search "no-citations" outcome**: the spec is correct but
  the content isn't being cited — a content-strategy problem (out
  of library scope), not a schema problem.

## References

- `references/schema-org-types.md` — the per-page-type Schema.org
  shape mappings + Zod schema templates.
- `references/json-ld-generators.md` — TypeScript template for
  the `src/lib/schema/<type>.ts` generators with framework-
  specific server-side injection.
- `references/aeo-conventions.md` — AI-search citation discipline
  conventions (question-answer structure, Author / dateModified
  properties, canonical-URL discipline) + per-engine quirks
  (Perplexity / ChatGPT-search / Gemini).
