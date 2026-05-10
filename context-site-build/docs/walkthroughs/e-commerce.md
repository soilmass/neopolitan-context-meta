# Walkthrough — e-commerce site

A site with catalog + cart + checkout. Adds product schema,
inventory state, payments, transactional email beyond what a
marketing site needs.

**Typical timeline**: 12-18 weeks. Heavier on Phase 2 (Requirements)
and Phase 7 (Post-launch optimization) than marketing sites.

**Default stack**: Combo A (Next.js + Vercel + Sanity + R3F + GSAP)
OR Combo B (Nuxt 3) — both have mature e-commerce SDK ecosystems
(Next.js + Shopify Hydrogen / Medusa; Nuxt + Vue Storefront).

---

## What's different from a marketing site

| Concern | Marketing site | E-commerce |
|---|---|---|
| Backend complexity | Low (CMS reads only) | High (cart state, inventory, payments) |
| State management | None client-side | Cart state + auth state |
| Real-time | None | Stock-level + price updates |
| Payments | None | Stripe / Adyen / Shopify Checkout |
| Email | Marketing (Loops) | Transactional + Marketing (Resend + Loops) |
| Schema.org | Organization + WebSite | Product (load-bearing) + Offer + Review + BreadcrumbList |
| Analytics | Marketing funnel | Marketing funnel + commerce funnel + cart-abandonment |
| Privacy | Light cookie consent | Full GDPR/CCPA + payment-data PCI scope |

---

## Phase 1 — Discovery (2-3 weeks)

Same atoms as marketing-site walkthrough, with these additions:

- **`persona-author`** is **load-bearing** for e-commerce — segment
  by purchase intent + price sensitivity + frequency.
- **`kpi-author`** includes commerce-funnel KPIs: AOV (average order
  value), conversion rate, cart-abandonment rate, repeat-purchase rate,
  CAC / LTV.
- **`ost-author`** is more useful for e-commerce than for static
  marketing — opportunity trees per acquisition channel + per
  conversion-stage.

---

## Phase 2 — Requirements (2-3 weeks; heavier than marketing)

| Atom | E-commerce-specific notes |
|---|---|
| `srs-author` | Adds inventory-consistency NFRs, payment-flow latency NFRs (≤ 2s p95 from cart-submit to payment-redirect), webhook delivery guarantees. Bundle budget per `performance-budget-author` Product-page-type row (PDP is typically ≤ 200 KB critical JS due to image-heavy renders). |
| `adr-author` × 12-15 | The 8 Combo-A ADRs + commerce-specific: payments processor (Stripe vs Adyen vs Shopify Checkout); cart persistence (cookie vs server session vs hybrid); inventory consistency model (eventual vs strong); SKU cardinality + CMS modeling; tax + shipping calculation strategy; refund + return workflow; subscription vs one-time payments. |
| `threat-model-author` | E-commerce threat surfaces: payment fraud (BIN attack, card-testing); cart-injection; price-manipulation via client-side; inventory exhaustion; PCI scope; reauth on checkout. |
| `privacy-plan-author` | Full GDPR/CCPA flows; cookie consent before any analytics; payment-data PCI-DSS scope (processor takes most of it; document the boundary). |

**Cross-cutting setup**:

- `analytics-instrumentation-author` — commerce events: `view_product`,
  `add_to_cart`, `start_checkout`, `complete_purchase`, `refund`. Per-
  event property schemas include `cart_total`, `currency`, `sku`,
  `quantity`.
- `aeo-schema-author` — **Product schema is load-bearing** for SEO; CI
  must validate every PDP's JSON-LD against Schema.org Product.
- `i18n-strategy-author` — typically required for e-commerce expanding
  internationally; `inLanguage` + `priceCurrency` per locale.
- `performance-budget-author` — PDP budget row is the strictest; the
  product-listing-page (PLP) row also.
- `error-monitoring-setup-author` — observability is more rigorous;
  cart errors surface as P1; payment errors as P0.
- `release-discipline-author` — feature flags load-bearing for cart-
  feature rollouts (you cannot rollback a deployed checkout flow if
  customers are mid-cart).

---

## Phase 3 — Design (4-5 weeks; heavier than marketing)

Same atoms as marketing-site walkthrough, with these additions:

- **`component-states-matrix-author`** — the 9-state matrix for
  Product / Cart / Checkout components is load-bearing; CI cannot
  pass without all 9 states for these.
- **`a11y-annotations-author`** — purchase-flow a11y is rigorous
  (single-pointer alternatives for drag-to-add-to-cart; focus-visible
  parity in the cart-modal; keyboard-navigable checkout form).
- **`prototype-author`** — the checkout prototype goes through usability
  testing more rigorously than marketing pages.

---

## Phase 4 — Build (4-6 weeks)

Engineering-led; the library doesn't ship Phase 4 atoms.

**Continuous discovery** (`discovery-tick-author`) for e-commerce is
heavier — weekly digest of cart-abandonment + checkout-error +
analytics signals.

---

## Phase 5 — Hardening (2 weeks; rigorous)

| Atom | E-commerce-specific notes |
|---|---|
| `runbook-author` × 4 | Deployment + incident + launch + **payment-incident** runbook (the dedicated "Stripe webhook backlog" / "PSP outage" runbook). |
| `motion-conformance-author` | Same as marketing; +cart-modal motion criteria. |
| `conformance-statement-author` | E-commerce conformance is heavier — purchase-flow keyboard pass + screen-reader pass mandatory; document is more thorough. |
| `polish-discipline-author` | Optional; less common for e-commerce since the polish budget often goes to checkout-flow optimization instead. |

---

## Phase 6 — Launch (1 week)

| Atom | Notes |
|---|---|
| `launch-comms-author` | Marketing announcement + transactional-email-template launch + status-page initial post. The e-commerce launch is gated on a dry-run purchase end-to-end. |

**Pre-launch dry-run**: 5 test purchases through the checkout in
production-mode (with refund afterwards). Per `release-discipline-
author` go/no-go: each test purchase is a checklist gate.

---

## Phase 7 — Post-launch (ongoing; heavier than marketing)

E-commerce's Phase 7 atoms are invoked at higher cadence than
marketing:

- **`hypercare-digest-author`** — daily for first 4-8 weeks (longer
  than marketing).
- **`optimization-loop-author`** — load-bearing; e-commerce lives or
  dies on conversion-rate experiments.
- **`optimization-backlog-author`** — weekly; experiments backed by
  RICE-scored hypotheses.
- **`weekly-metric-report-author`** — load-bearing; commerce metrics
  (AOV, conversion rate, cart-abandonment) reviewed weekly.
- **`win-regression-report-author`** — invoked when an experiment
  unexpectedly degrades a metric; common in e-commerce.

**Atoms invoked specifically for e-commerce**:

- **`aeo-baseline-author`** at T+8wk and T+24wk — Product schema's
  Rich Results impact takes 2-3 months to surface in Google Search
  Console + AI-search citations.

---

## Atom-skip table for small e-commerce (≤ 50 SKUs)

| Phase | Required atoms |
|---|---|
| 1 | vision-author, persona-author, kpi-author, stakeholder-map-author |
| 2 | srs-author, adr-author × 8-10, threat-model-author, privacy-plan-author, master-schedule-author, performance-budget-author, analytics-instrumentation-author, aeo-schema-author, error-monitoring-setup-author, release-discipline-author |
| 3 | mood-board-author, art-direction-author, motion-language-author (if motion-heavy), design-tokens-author, design-system-author, component-states-matrix-author, a11y-annotations-author, engineering-handoff-spec-author |
| 4 | (engineering builds) |
| 5 | runbook-author × 3 (deployment, incident, payment-incident), motion-conformance-author, conformance-statement-author |
| 6 | launch-comms-author |
| 7 | baseline-report-author, hypercare-digest-author, weekly-metric-report-author, optimization-loop-author, optimization-backlog-author |

Skip OST + risk-register at this scale; revisit if scaling.

---

## See also

- `walkthroughs/marketing-site.md` — for non-commerce marketing sites.
- `walkthroughs/web-app.md` — for CRUD-heavy app shells (e.g., the
  back-office complement to e-commerce).
- `LIBRARY-MAP.md` — dependency graph.
- `examples/outputs/` — anonymized outputs (the e-commerce variants
  cite Product schema + commerce events).
