# KPIs — `<project>` (anonymized example output)

> **Note**: anonymized illustrative output of `kpi-author`. KPIs map
> to events in `analytics-spec.md`; thresholds align with vision in
> `vision.md`.

---

## North Star

**Active sites** — number of users with a published portfolio that
received ≥ 1 visit in the last 30 days.

| Cadence | Value | Trend |
|---|---|---|
| 6-month target | `<n-low>` | — |
| 12-month target | `<n-medium>` | — |
| 24-month target | `<n-high>` | — |

Why this metric: it captures product fit (someone uses it) +
distribution (someone visits it). Either alone is incomplete.

---

## Acquisition KPIs

| KPI | Definition | Threshold | Event source |
|---|---|---|---|
| Signup rate | `start_signup` → `complete_signup` | ≥ 60% | `analytics-spec.md` events `start_signup` / `complete_signup` |
| Activation rate | `complete_signup` → `publish_first_site` | ≥ 40% | events `publish_site` |
| Time-to-publish (median) | `complete_signup` → `publish_first_site` | ≤ 30 minutes | derived from event timestamps |
| Marketing-channel attribution | `view_marketing_page` → `start_signup` per channel | ≥ 5% organic; ≥ 2% paid | event `start_signup` with `referrer` property |

---

## Engagement KPIs

| KPI | Definition | Threshold |
|---|---|---|
| 7-day retention | `complete_signup` users active 7 days later | ≥ 35% |
| 30-day retention | `complete_signup` users active 30 days later | ≥ 25% |
| Edits per active user / week | `edit_*` events / unique active users | ≥ 3 |
| Sites with custom domain | `complete_custom_domain_setup` / `publish_first_site` | ≥ 30% |

Custom-domain rate is a leading indicator of users-who-take-it-
seriously; it correlates with retention.

---

## Conversion / monetization KPIs

| KPI | Definition | Threshold |
|---|---|---|
| Free-to-paid conversion | `complete_signup` → `complete_first_payment` | ≥ 5% |
| MRR (monthly recurring revenue) | sum of active subscriptions | `<dollar-amount-month-6>` (6mo); `<dollar-amount-month-12>` (12mo) |
| LTV (lifetime value, est.) | average revenue × estimated lifespan | `<dollar-amount>` |
| CAC (customer acquisition cost) | marketing-spend / paid-conversions | ≤ `<dollar-amount>` |
| LTV / CAC ratio | LTV / CAC | ≥ 3 (industry healthy threshold) |

---

## Site-quality KPIs (production sites the platform hosts)

| KPI | Definition | Threshold | Source |
|---|---|---|---|
| LCP p75 across all hosted sites | aggregated CWV p75 | ≤ 2.0s | Vercel Speed Insights |
| INP p75 across all hosted sites | aggregated CWV p75 | ≤ 200ms | Vercel Speed Insights |
| CLS p75 across all hosted sites | aggregated CWV p75 | ≤ 0.05 | Vercel Speed Insights |
| Site error rate | % of page-views with uncaught error | ≤ 0.5% | Sentry custom dashboard |
| Site uptime | % of page-views successfully served | ≥ 99.9% | Vercel Edge logs aggregated |

Per `observability-spec.md` SLI definitions; per
`performance-budget.md` CI gates.

---

## NPS / qualitative KPIs

| KPI | Definition | Cadence | Threshold |
|---|---|---|---|
| Net Promoter Score | post-30-day-survey | quarterly | ≥ 40 (industry SaaS healthy) |
| Customer satisfaction (CSAT) | per-support-ticket exit survey | continuous | ≥ 4.5 / 5 |
| Feature-request volume | tagged tickets per feature | weekly digest | informational; signal for `optimization-loop-author` |

Sources:
- NPS via `analytics-spec.md` event `submit_nps`.
- CSAT via support-tool integration (Intercom / Zendesk).
- Feature requests via `discovery-tick-author` weekly digest.

---

## AEO / AI-search KPIs

| KPI | Definition | Threshold | Cadence |
|---|---|---|---|
| AI-search citation count | mentions across Perplexity / ChatGPT-search / Gemini | ≥ 5 / month at 6mo | monthly via `aeo-baseline-author` |
| Schema.org valid pages | % of pages passing Rich Results Test | 100% | weekly via CI |
| Search Console click-through rate | impressions → clicks | ≥ 3% (industry healthy) | weekly Search Console pull |

Per `aeo-schema-spec.md` (the structured-data spec) +
`aeo-baseline-author` (the measurement output).

---

## Reporting cadence

| Report | Cadence | Author |
|---|---|---|
| Hypercare digest | daily (first 4 weeks post-launch) | `hypercare-digest-author` |
| Weekly metric report | weekly | `weekly-metric-report-author` |
| Monthly stakeholder report | monthly | `monthly-stakeholder-report-author` |
| QBR | quarterly | `quarterly-business-review-author` |
| Annual retro | yearly | `annual-retrospective-author` |
| AEO baseline | T+8wk + monthly thereafter | `aeo-baseline-author` |

Each report cites this `kpis.md` document by URL/section so the
reader knows the threshold context.

---

## Threshold-revision history

KPIs are not frozen — when a threshold proves consistently wrong,
this document gets a PATCH bump revising it.

| Date | Change | Reason |
|---|---|---|
| 2026-05-08 | Initial v0.1.0 | Authored at Phase 1. |

---

## Authority

- Vision: `vision.md` v0.2 (signed 2026-04-23).
- Personas: `personas.md` v0.1.
- OST: `ost.md` v0.1 (the opportunity-tree that decomposes these
  KPIs into testable hypotheses).

---

*Authored 2026-04-25 by kpi-author v0.1.0. Reviewed 2026-04-30 by
founding team. Sign-off: 2026-05-01.*
